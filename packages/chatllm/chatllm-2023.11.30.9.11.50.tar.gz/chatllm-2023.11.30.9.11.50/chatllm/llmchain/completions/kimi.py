#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : kimi
# @Time         : 2023/11/29 17:00
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.cache_utils import ttl_cache
from meutils.decorators.retry import retrying

from chatllm.llmchain.utils import tiktoken_encoder
from chatllm.schemas.kimi.protocol import EventData, State

from openai.types.chat import chat_completion_chunk, chat_completion

post = retrying(requests.post)


class Completions(object):
    def __init__(self, **client_params):
        self.client_params = client_params

    def create(
        self,
        messages: List[Dict[str, Any]],  # [{'role': 'user', 'content': '讲个故事'}] "refs": ['xx'], "use_search": False
        **creat_kwargs,
    ):
        api_key = self.client_params.pop('api_key')

        if self.client_params.get('stream'):
            return self._stream_create(messages, api_key, **creat_kwargs)
        else:
            return self._create(messages, api_key, **creat_kwargs)

    def _create(self, messages, api_key, **kwargs):
        chunk_id = f"chatcmpl-{uuid.uuid1()}"
        created = int(time.time())
        model = kwargs.get('model', 'kimi')
        # todo
        # response = requests.post(url, json=json_str, headers=headers)
        # response.encoding = 'utf-8'
        # response.text.strip().split('\n\n')

        content = ''
        for chunk in self._stream_create(messages, api_key, **kwargs):
            content += chunk.choices[0].delta.content

        message = chat_completion.ChatCompletionMessage(role='assistant', content=content or '授权过期')

        choice = chat_completion.Choice(
            index=0,
            message=message,
            finish_reason='stop'
        )

        prompt_tokens, completion_tokens = map(len, tiktoken_encoder.encode_batch([str(messages), content]))
        total_tokens = prompt_tokens + completion_tokens

        usage = chat_completion.CompletionUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens
        )

        completion = chat_completion.ChatCompletion(
            id=chunk_id,
            choices=[choice],
            created=created,
            model=model,
            object="chat.completion",
            usage=usage

        )

        return completion

    def _stream_create(self, messages, api_key, **kwargs):
        chunk_id = f"chatcmpl-{uuid.uuid1()}"
        created = int(time.time())
        model = kwargs.get('model', 'kimi')

        refs = kwargs.pop('refs', [])
        use_search = False if refs else kwargs.pop('use_search', True)

        headers = {
            'Authorization': f"Bearer {api_key}",  # access_token
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }

        url = self._create_url(api_key=api_key, **kwargs)
        response = post(
            url,
            headers=headers,
            stream=True,
            json={'messages': messages, "refs": refs, "use_search": use_search},
        )

        # todo: 抽象出去
        buffer = b''  # 用于缓存不完整的行
        for chunk in response.iter_content(chunk_size=8096):  # , decode_unicode=True
            if chunk:
                buffer += chunk
                lines = buffer.split(b'\n\n')  # 按照两个换行符切分
                buffer = lines.pop()  # 最后一行可能不完整，保存到 buffer 中
                for line in lines:
                    line = line.decode('utf-8').strip("data: ")
                    # logger.debug(line)
                    event_data = EventData(**json.loads(line))

                    # openai
                    delta = chat_completion_chunk.ChoiceDelta(role='assistant', content=event_data.text)
                    choice = chat_completion_chunk.Choice(
                        index=0,
                        delta=delta,
                        finish_reason="stop" if event_data.event == 'all_done' else None
                    )

                    chunk = chat_completion_chunk.ChatCompletionChunk(
                        id=chunk_id,
                        choices=[choice],
                        created=created,
                        model=model,
                        object="chat.completion.chunk"
                    )
                    yield chunk

    @staticmethod
    @retrying
    @ttl_cache(ttl=1 * 24 * 3600)
    def _create_url(api_key, conversation_name="Xchat", **kwargs):
        headers = {
            'Authorization': f"Bearer {api_key}",  # access_token
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        url = "https://kimi.moonshot.cn/api/chat"
        payload = {"name": conversation_name, "is_example": False}
        response = requests.post(url, json=payload, headers=headers).json()
        logger.debug(response)

        conversation_id = response.get('id')
        return f"{url}/{conversation_id}/completion/stream"

    @staticmethod
    @retrying
    @ttl_cache(ttl=30)
    def load_state(self, state_file):
        state = State(**json.loads(Path(state_file).read_text()))
        refresh_token = state.origins[0].localStorage[1].value
        access_token = state.origins[0].localStorage[2].value
        return access_token


if __name__ == '__main__':
    api_key = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlY2hvbWluZC1hcGktYXBpIiwiZXhwIjoxNzAxMjU5MzkxLCJpYXQiOjE3MDEyNTg0OTEsImp0aSI6ImNsamk5dXQwdGMxYW9sdHJmcDJnIiwidHlwIjoiYWNjZXNzIiwic3BhY2VfaWQiOiJja2kwOTRiM2Flc2xnbGo2Zm8yZyIsInN1YiI6ImNraTA5NGIzYWVzbGdsajZmbzMwIn0.vozCaeY617uiUotVJeJ7merXr8Q92J5l8qj_JjMRWCdCuN-LEnoydmJNxDlY0T6GBxsezHH49Rbug8nq5GDV_g'
    completion = Completion(api_key=api_key, stream=False)
    r = completion.create(
        messages=[{'role': 'user', 'content': '你是谁'}]
    )
    print(r)
