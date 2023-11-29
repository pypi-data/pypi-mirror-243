import base64
import json
from typing import TypeVar, Type, Any, TypedDict, Dict, Callable, List, Optional
from typing_extensions import Unpack, NotRequired
from dacite import from_dict, Config
from .decorators import log

_DataModel = TypeVar("_DataModel")

__all__ = ('http', 'cloud_event')

class ParseOptions(TypedDict):
    type_hooks: NotRequired[Dict[Type, Callable[[Any], Any]]]
    cast: NotRequired[List[Type]]
    forward_references: NotRequired[Optional[Dict[str, Any]]]
    check_types: NotRequired[bool]
    strict: NotRequired[bool]
    strict_unions_match: NotRequired[bool]

def internal_parse_data(data, Model: Type[_DataModel], **kwargs) -> _DataModel:
    if Model == dict:
        return data
    try:
        from pydantic import BaseModel
        if issubclass(Model, BaseModel):
            return Model(**data)
    except:
        pass
    instance: Any = from_dict(Model, data, Config(**kwargs))
    return instance


@log(0, name = "parse_request.http")
def http(request, Model: Type[_DataModel], **kwargs: Unpack[ParseOptions]) -> _DataModel:
    print(f"{request=}")
    request_body = request.get_json(silent=True)  or {}
    print(f"{request_body=}")
    data: Any = request_body
    print(f"{data=}")
    return internal_parse_data(data, Model, **kwargs)

@log(0, name = "parse_request.cloud_event")
def cloud_event(cloud_event, Model: Type[_DataModel], **kwargs: Unpack[ParseOptions]) -> _DataModel:
    cloud_event_data = cloud_event.data['message']['data']
    decoded_event = base64.b64decode(cloud_event_data)
    print(f"{decoded_event=}")
    event_data_string = decoded_event.decode('utf-8')
    print(f"{event_data_string=}")

    data = json.loads(event_data_string)
    return internal_parse_data(data, Model, **kwargs)
