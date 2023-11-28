import inspect
from types import NoneType, UnionType
from typing import Type, get_origin

from pydantic import BaseModel
from pydantic.fields import FieldInfo

from .enums import TYPE_MAPPING
from .models import Message, Field


def parse_type_sequence(name: str, python_type, args: list) -> Field:
    if len(args) != 1:
        raise TypeError(
            f"Field '{name}': type '{python_type}' must have only one subtype, not {len(args)}.",
        )

    inside_python_type = args[0]
    if (origin := get_origin(inside_python_type)) is not None:
        inside_args = list(inside_python_type.__args__)
        if origin is UnionType:
            return parse_type_union(name, inside_python_type, inside_args)
        else:
            raise TypeError(
                f"Field '{name}': unsupported type '{origin}' in '{inside_python_type}.",
            )
    if inside_python_type in TYPE_MAPPING:
        grpc_type = TYPE_MAPPING[inside_python_type].value
    elif inspect.isclass(inside_python_type) and issubclass(inside_python_type, BaseModel):
        grpc_type = inside_python_type.__name__
    else:
        raise TypeError(
            f"Field '{name}': unsupported type '{inside_python_type}' in type '{python_type}'.",
        )

    return Field(name=name, type=grpc_type, repeated=True)


def parse_type_mapping(name: str, python_type, args: list) -> Field:
    if len(args) != 2:
        raise TypeError(
            f"Field '{name}': type '{python_type}' must have two subtype, not {len(args)}.",
        )

    grpc_type = TYPE_MAPPING[dict].value
    python_map_key, python_map_value = args
    map_key, map_value = None, None
    if python_map_key in TYPE_MAPPING:
        map_key = TYPE_MAPPING[python_map_key].value
    else:
        raise TypeError(
            f"Field '{name}': unsupported type '{python_map_key}' in '{python_type}'.",
        )
    if python_map_value in TYPE_MAPPING:
        map_value = TYPE_MAPPING[python_map_value].value
    elif inspect.isclass(python_map_value) and issubclass(python_map_value, BaseModel):
        map_value = python_map_value.__name__
    else:
        raise TypeError(
            f"Field '{name}': unsupported type '{python_map_value}' in '{python_type}'.",
        )

    return Field(
        name=name,
        type=grpc_type,
        map_key=map_key,
        map_value=map_value,
    )


def parse_type_union(name: str, python_type, args: list) -> Field:
    if NoneType in args:
        args.remove(NoneType)
    if len(args) != 1:
        raise TypeError(
            f"Field '{name}': type '{python_type}' must have only one subtype , not {len(args)}. "
            "Tip: None/Optional type ignoring."
        )

    inside_python_type = args[0]
    if (origin := get_origin(inside_python_type)) is not None:
        inside_args = list(inside_python_type.__args__)
        if origin is UnionType:
            return parse_type_union(name, inside_python_type, inside_args)
        else:
            raise TypeError(
                f"Field '{name}': unsupported type '{inside_python_type}' in '{python_type}'.",
            )
    if inside_python_type in TYPE_MAPPING:
        grpc_type = TYPE_MAPPING[inside_python_type].value
    elif inspect.isclass(inside_python_type) and issubclass(inside_python_type, BaseModel):
        grpc_type = inside_python_type.__name__
    else:
        raise TypeError(
            f"Field '{name}': unsupported type '{inside_python_type}' in {python_type}'.",
        )

    return Field(name=name, type=grpc_type)


def parse_field(name: str, field: FieldInfo) -> Field:
    repeated = False
    map_key, map_value = None, None
    python_type = field.annotation
    if (origin := get_origin(python_type)) is not None:
        args = list(python_type.__args__)
        if issubclass(origin, (list, tuple, set, frozenset)):
            return parse_type_sequence(name, python_type, args)
        elif issubclass(origin, dict):
            return parse_type_mapping(name, python_type, args)
        elif origin is UnionType:
            return parse_type_union(name, python_type, args)
        else:
            raise TypeError(f"Field '{name}': unknown origin '{origin}' in type '{python_type}'.")

    if not inspect.isclass(python_type):
        raise TypeError(f"Field '{name}': must be a type, not a '{python_type}'.")
    if python_type in TYPE_MAPPING:
        grpc_type = TYPE_MAPPING[python_type].value
    else:
        raise TypeError(f"Field '{name}': unsupported type '{python_type}'.")

    return Field(
        name=name,
        repeated=repeated,
        type=grpc_type,
        map_key=map_key,
        map_value=map_value,
    )


def get_message_from_model(model: Type[BaseModel]) -> Message:
    fields = {}

    for name, field in model.__fields__.items():
        fields[name] = parse_field(name=name, field=field)

    return Message(name=model.__name__, fields=fields)


def gather_models(model: Type[BaseModel]) -> set[Type[BaseModel]]:
    models = set()
    stack = [model]
    processed = set()

    while stack:
        model = stack.pop()
        models.add(model)
        processed.add(model)
        
        for field in model.__fields__.values():
            arg_stack = [field.annotation]
            while arg_stack:
                arg = arg_stack.pop()
                if get_origin(arg) is not None:
                    arg_stack.extend(arg.__args__)
                elif (
                        inspect.isclass(arg) and
                        issubclass(arg, BaseModel) and
                        arg not in processed and
                        arg not in stack
                ):
                    stack.append(arg)

    return models
