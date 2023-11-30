#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : protocol
# @Time         : 2023/11/29 16:45
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *


class Cookie(BaseModel):
    name: str
    value: str
    domain: str
    path: str
    expires: float
    httpOnly: bool
    secure: bool
    sameSite: str


class StorageItem(BaseModel):
    name: str
    value: str


class Origin(BaseModel):
    origin: str
    localStorage: List[StorageItem]


class State(BaseModel):
    """
        state = State(**json.loads(Path('state.json').read_text()))
        refresh_token = state.origins[0].localStorage[1].value
        access_token = state.origins[0].localStorage[2].value
    """
    cookies: List[Cookie]
    origins: List[Origin]


class SearchMessage(BaseModel):
    need2search: bool
    search_target: str
    search_language: str


class EventData(BaseModel):
    """
    data: {"content":"1+1","event":"req","group_id":"cljdett0tc12f8jcpc7g","id":"cljdett0tc12f8jcpc8g","refs":[]}
    data: {"event":"resp","group_id":"cljdett0tc12f8jcpc7g","id":"cljdett0tc12f8jcpc90"}
    data: {"event":"debug","message":{"need2search":false,"search_target":"","search_language":""}}
    data: {"event":"debug","message":{"need2search":true,"search_target":"南京今天天气","search_language":"zh-cn"}}
    data: {"event":"search_plus","msg":{"type":"start"}}
    data: {"event":"search_plus","msg":{"successNum":1,"title":"南京天气","type":"get_res","url":"http://m.nmc.cn/publish/forecast/AJS/nanjing.html"}}

    data: {"event":"cmpl","text":" "}
    data: {"event":"cmpl","text":"1"}
    data: {"event":"cmpl","text":"å "}
    data: {"event":"done"}
    data: {"event":"cmpl","text":"1"}
    data: {"event":"cmpl","text":"ç­"}
    data: {"event":"cmpl","text":"äº"}
    data: {"event":"cmpl","text":"2"}
    data: {"event":"cmpl","text":"ã"}
    data: {"event":"all_done"}
    """
    event: Optional[Literal["req", "resp", "debug", "search_plus", "cmpl", "done", "all_done"]] = None
    content: Optional[str] = None

    id: Optional[str] = None
    group_id: Optional[str] = None

    message: Optional[SearchMessage] = None
    msg: Optional[dict] = None
    refs: List[str] = []

    text: str = ''

    # json_str = {"messages": [{"role": "system", "content": "你现在扮演的角色是初中老师"},
    #                          {"role": "user", "content": "你现在扮演的角色是？"}], "refs": [], "use_search": False}


if __name__ == '__main__':
    state = State(**json.loads(Path('state.json').read_text()))
    refresh_token = state.origins[0].localStorage[1].value
    access_token = state.origins[0].localStorage[2].value
