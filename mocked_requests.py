import random
from typing import Protocol, runtime_checkable


PYJSON_VALUE_TYPES = str | int | dict | list | bool | float


class AbstractResponse(Protocol):
    status_code: int
    
    def json(self) -> dict[str, PYJSON_VALUE_TYPES]:
        pass


class AbstractRequester(Protocol):
    def post(self, url: str, json: dict[str, PYJSON_VALUE_TYPES], headers: dict[str, str]) -> AbstractResponse:
        pass


class Requests:
    class Response:
        def __init__(self): 
            self.status_code = 500 if random.random() > 0.9 else 200
            
        def json(self) -> dict[str, PYJSON_VALUE_TYPES]:
            return {"hasFoulLanguage": False if random.random() > 0.25 else True}

    def post(self, url: str, json: dict[str, PYJSON_VALUE_TYPES], headers: dict[str, str]) -> AbstractResponse:
        return Requests.Response()

requests = Requests()

