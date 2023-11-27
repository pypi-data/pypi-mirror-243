from typing import Any
from any_serde.common import JSON, JSONPrimitive, InvalidDeserializationException, InvalidSerializationException


def validate_json(data: Any) -> JSON:
    if isinstance(data, JSONPrimitive):
        return data

    if isinstance(data, list):
        return [validate_json(child) for child in data]

    if isinstance(data, dict):

        def assert_str(x: Any) -> str:
            if isinstance(x, str):
                return x
            raise ValueError()

        return {assert_str(key): validate_json(value) for key, value in data.items()}

    raise ValueError()


def from_data(data: JSON) -> JSON:
    try:
        return validate_json(data)
    except ValueError as err:
        raise InvalidDeserializationException from err


def to_data(obj: JSON) -> JSON:
    try:
        return validate_json(obj)
    except ValueError as err:
        raise InvalidSerializationException from err
