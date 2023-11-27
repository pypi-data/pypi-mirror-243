""" A Serializable Dataclass Implementation """
from __future__ import annotations

import dataclasses
import functools
import os
from typing import Any, Dict, Optional, Type, TypeVar, get_type_hints
from any_serde.common import (
    JSON,
    InvalidDeserializationException,
)


ATTR_SERIALIZATION_RENAMES = "__serialization_renames__"
ATTR_UNKNOWN_DATA_KEYS_POLICY = "__unknown_data_keys_policy__"
ATTR_INJECTED_DATA = "__injected_data__"


T_Dataclass = TypeVar("T_Dataclass", bound=object)


def is_dataclass_type(typ: Any) -> bool:
    return isinstance(typ, type) and dataclasses.is_dataclass(typ)


@functools.lru_cache(None)
def _get_type_hints(typ: Type[object]) -> Dict[str, Type[Any]]:
    return get_type_hints(typ)


def _field_is_required(field: dataclasses.Field) -> bool:
    if not isinstance(field.default, dataclasses._MISSING_TYPE):
        return False

    if not isinstance(field.default_factory, dataclasses._MISSING_TYPE):
        return False

    return True


@functools.lru_cache(None)
def _get_serialization_renames(dataclass_type: Type[T_Dataclass]) -> Dict[str, str]:
    error_msg_start = f"Illegal {ATTR_SERIALIZATION_RENAMES} value for {dataclass_type}!"

    serialization_renames = getattr(dataclass_type, ATTR_SERIALIZATION_RENAMES, {})
    if not isinstance(serialization_renames, dict):
        raise AssertionError(f"{error_msg_start} Not a dictionary!")

    for attribute_key, data_key in serialization_renames.items():
        if not isinstance(attribute_key, str) or not isinstance(data_key, str):
            raise AssertionError(f"{error_msg_start} Found non-string values!")

    attribute_keys = set(serialization_renames)
    data_keys = set(serialization_renames.values())
    if len(data_keys) < len(attribute_keys):
        raise AssertionError(f"{error_msg_start} Duplicate data keys!")

    dataclass_field_names = {field.name for field in dataclasses.fields(dataclass_type)}  # type: ignore[arg-type]
    if attribute_keys - dataclass_field_names:
        raise AssertionError(f"{error_msg_start} Mapping attributes that don't exist!")

    unmapped_attribute_keys = dataclass_field_names - attribute_keys
    if unmapped_attribute_keys & data_keys:
        raise AssertionError(f"{error_msg_start} Data keys conflict with existing fields!")

    return serialization_renames


@functools.lru_cache(None)
def _get_unknown_data_keys_policy(dataclass_type: Type[T_Dataclass]) -> UnknownDataKeysPolicy:
    if not hasattr(dataclass_type, ATTR_UNKNOWN_DATA_KEYS_POLICY):
        return UnknownDataKeysPolicy(
            allow=False,
            roundtrip=False,
        )

    policy = getattr(dataclass_type, ATTR_UNKNOWN_DATA_KEYS_POLICY)

    assert isinstance(policy, UnknownDataKeysPolicy), "Bad data keys policy"

    return policy


def from_data(type_: Type[T_Dataclass], data: JSON) -> T_Dataclass:
    if not isinstance(data, dict):
        raise InvalidDeserializationException(f"Dataclasses serialize to dict. Got {type(data)} instead!")

    assert is_dataclass_type(type_), "Can only call dataclass_serde.from_data on dataclass types!"
    injected_data: Optional[Dict[str, JSON]] = None

    field_types = _get_type_hints(type_)  # type: ignore
    dataclass_fields = {x.name: x for x in dataclasses.fields(type_)}  # type: ignore

    fields_without_types = set(dataclass_fields) - set(field_types)
    assert not fields_without_types, f"Fields without types: {fields_without_types}"

    serialization_renames = _get_serialization_renames(type_)  # type: ignore[arg-type]
    deserialization_renames = {data_key: attribute_key for attribute_key, data_key in serialization_renames.items()}
    mapped_data = {deserialization_renames.get(data_key, data_key): data_value for data_key, data_value in data.items()}

    data_keys_without_fields = set(mapped_data) - set(dataclass_fields)
    if data_keys_without_fields:
        unknown_data_keys_policy = _get_unknown_data_keys_policy(type_)  # type: ignore[arg-type]
        if not unknown_data_keys_policy.allow:
            # TODO: not intuitive that these printed are after mapping. Either print before map or explain.
            raise InvalidDeserializationException(
                f"Parsing {type_}, got data keys without fields: {data_keys_without_fields}"
            )

        if unknown_data_keys_policy.roundtrip:
            injected_data = {data_key: mapped_data[data_key] for data_key in data_keys_without_fields}

        mapped_data = {
            mapped_key: mapped_value
            for mapped_key, mapped_value in mapped_data.items()
            if mapped_key in dataclass_fields
        }

    required_field_names = [field_name for field_name, field in dataclass_fields.items() if _field_is_required(field)]

    missing_required_fields = set(required_field_names) - set(mapped_data)
    if missing_required_fields:
        raise InvalidDeserializationException(f"Data is missing required fields: {missing_required_fields}")

    from any_serde import serde

    casted_data = {
        field_name: serde.from_data(field_types[field_name], field_data)
        for field_name, field_data in mapped_data.items()
    }

    obj = type_(**casted_data)

    if injected_data is not None:
        setattr(obj, ATTR_INJECTED_DATA, injected_data)

    return obj


def to_data(type_: Type[T_Dataclass], item: T_Dataclass) -> JSON:
    type_ = type(item)

    assert is_dataclass_type(type_), "Can only call dataclass_serde.to_data on dataclass instances!"

    field_types = _get_type_hints(type_)  # type: ignore
    dataclass_field_names = {x.name for x in dataclasses.fields(type_)}  # type: ignore

    fields_without_types = set(dataclass_field_names) - set(field_types)
    assert not fields_without_types, f"Fields without types: {fields_without_types}"

    serialization_renames = _get_serialization_renames(type_)  # type: ignore[arg-type]

    from any_serde import serde

    data = {
        serialization_renames.get(field_name, field_name): serde.to_data(
            field_types[field_name], getattr(item, field_name)
        )
        for field_name in dataclass_field_names
    }

    if hasattr(item, ATTR_INJECTED_DATA):
        injected_data = getattr(item, ATTR_INJECTED_DATA)
        assert isinstance(injected_data, dict)
        assert not set(injected_data) & set(data), "Trying to inject over existing keys"
        data.update(injected_data)

    return data


def register_serialization_renames(serialization_renames: Dict[str, str], type_: T_Dataclass) -> None:
    """Allows the serialization for a dataclass to have different keys than the dataclass."""
    # TODO: validate serialization renames here as well
    setattr(type_, ATTR_SERIALIZATION_RENAMES, serialization_renames)


@dataclasses.dataclass
class UnknownDataKeysPolicy:
    allow: bool
    roundtrip: bool


def allow_unknown_data_keys(type_: T_Dataclass, *, roundtrip: bool) -> None:
    policy = UnknownDataKeysPolicy(
        allow=True,
        roundtrip=roundtrip,
    )
    setattr(type_, ATTR_UNKNOWN_DATA_KEYS_POLICY, policy)


def dataclass_from_environ(
    dataclass_type: Type[T_Dataclass],
    environ: Optional[os._Environ] = None,
) -> T_Dataclass:
    if environ is None:
        environ = os.environ

    field_types = _get_type_hints(dataclass_type)  # type: ignore

    dataclass_args: Dict[str, JSON] = {}
    for field in dataclasses.fields(dataclass_type):  # type: ignore[arg-type]
        field_env_name = field.name.upper()
        if field_env_name not in environ:
            if _field_is_required(field):
                raise ValueError(f"Env var not set: {field_env_name}")
            continue

        raw_value: str = environ[field_env_name]
        value_type = field_types[field.name]

        if issubclass(value_type, str):
            parsed_value: JSON = raw_value
        elif issubclass(value_type, bool):
            parsed_value = bool(raw_value)
        elif issubclass(value_type, float):
            try:
                parsed_value = float(raw_value)
            except ValueError as err:
                raise InvalidDeserializationException from err
        elif issubclass(value_type, int):
            try:
                float_value = float(raw_value)
            except ValueError as err:
                raise InvalidDeserializationException from err
            int_value = int(float_value)
            if float_value != int_value:
                raise ValueError(f"Could not convert {raw_value} to int!")
            parsed_value = int_value
        else:
            raise ValueError(f"Cannot parse {value_type} from env vars yet!")

        dataclass_args[field.name] = parsed_value

    return dataclass_type(**dataclass_args)
