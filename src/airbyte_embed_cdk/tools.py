import json

from json import JSONDecodeError
from typing import Any, Iterable, Optional

from airbyte_cdk.models import AirbyteMessage, Type
from pydantic.main import BaseModel


def get_first(iterable: Iterable, predicate=lambda m: True):
    return next(filter(predicate, iterable), None)


def get_first_message(messages: Iterable[AirbyteMessage], message_type: Type) -> Optional[AirbyteMessage]:
    return get_first(messages, lambda m: m.type == message_type)


def write_json(file, obj) -> None:
    with open(file, "w") as f:
        if isinstance(obj, BaseModel):
            obj = json.loads(obj.json())
        json.dump(obj, f)


def read_json(file) -> Any:
    with open(file, "r") as f:
        return json.load(f)


def parse_json(line):
    try:
        return json.loads(line)
    except JSONDecodeError:
        return None


def pp_json(json_object):
    print(json.dumps(json_object, indent=2))
