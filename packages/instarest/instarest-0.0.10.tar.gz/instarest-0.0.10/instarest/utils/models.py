import inspect as ins
from pydantic import UUID4, validator
from typing import Any, Generator
from datetime import datetime
from enum import Enum as CoreEnum
from sqlalchemy import (
    Boolean,
    DateTime,
    UUID,
    String,
    Enum,
    inspect,
)
from instarest.db.base_class import DeclarativeBase

# support for pgvector without requiring it to be installed in instarest
try:
    from pgvector.sqlalchemy import Vector
    from numpy import ndarray
except ImportError:
    Vector = None
    ndarray = None


def remove_endstr(str: str, sub: str) -> str:
    if str.endswith(sub):
        return str[: -len(sub)]
    return str


def gen_column_attrs(
    ModelType: DeclarativeBase,
) -> Generator[tuple[str, tuple[type | Any, ...], dict[str, Any]], None, None]:
    """
    Generator for pulling attributes and types from the declared model.
    Includes foreign keys if actually saved in the table, but does not
    include attributes back-populated via relationships.

    **Parameters**

    * `ModelType`: A SQLAlchemy model class

    **Yields**
    * (field_name, (field_type, ...)) where field name is the name of the
    field (string) for this column, and field_type is the class
    of the type as it would be expected to be used in a
    pydantic schema.  "..." indicates no default in the schema.
    """
    mapper = inspect(ModelType)
    validators = {}
    for column in mapper.column_attrs:
        # name of the attribute, will be returned
        field_name = column.key

        # pull the actual attribute from the class
        field = getattr(ModelType, field_name)

        # find the type for being returned
        field_type = Any
        if isinstance(field.expression.type, UUID):
            field_type = UUID4

        if isinstance(field.expression.type, Boolean):
            field_type = bool

        if isinstance(field.expression.type, DateTime):
            field_type = datetime

        if isinstance(field.expression.type, String):
            field_type = str

        if isinstance(field.expression.type, Enum):
            field_type = CoreEnum

        if (
            Vector is not None
            and ndarray is not None
            and isinstance(field.expression.type, Vector)
        ):
            field_type = list[float]

            def numpy_to_list(cls, v):
                if isinstance(v, ndarray):
                    return v.tolist()
                return v

            validators[f"{field_name}_numpy_validator"] = validator(
                field_name, pre=True, always=True, allow_reuse=True
            )(numpy_to_list)

        yield field_name, (field_type, ...), validators


def dict_column_attrs_with_id(
    ModelType: DeclarativeBase, optional_fields: list[str] = []
) -> tuple[dict[str, tuple[type | Any | None, ...]], dict[str, Any]]:
    """
    Dictionary that gives same values as gen_column_attrs.
    If OptionalFields is provided, then those fields will be
    made optional in the output dictionary.

    **Parameters**

    See gen_column_attrs

    **Returns**

    dict generated from gen_column_attrs
    """

    output_fields = {}
    output_validators = {}
    for field_name, (field_type, _), validators in gen_column_attrs(ModelType):
        if field_name in optional_fields:
            output_fields[field_name] = (field_type | None, None)
        else:
            output_fields[field_name] = (field_type, ...)

        output_validators.update(validators)

    return output_fields, output_validators


def dict_optional_column_attrs_no_id(
    ModelType: DeclarativeBase,
) -> tuple[dict[str, tuple[type | Any | None, ...]], dict[str, Any]]:
    """
    Dictionary that gives same values as gen_column_attrs,
    except that every field_type is made optional (for use
    in base pydantic schemas) and "id" is removed (for use
    in base create/update pydantic schemas)

    **Parameters**

    See gen_column_attrs

    **Returns**

    dict generated from gen_column_attrs with "None" as the
    default value for pydantic schemas
    """

    output_fields = {}
    output_validators = {}
    for field_name, (field_type, _), validators in gen_column_attrs(ModelType):
        if field_name != "id":
            output_fields[field_name] = (field_type | None, None)
            output_validators.update(validators)

    return output_fields, output_validators


def gen_relationship_attrs(
    ModelType: DeclarativeBase, schema_list: list[object] = []
) -> Generator[tuple[str, tuple[type | Any, ...]], None, None]:
    """
    Generator for pulling attributes and types from the declared model.
    Includes foreign keys if actually saved in the table, but does not
    include attributes back-populated via relationships.

    **Parameters**

    * `ModelType`: A SQLAlchemy model class
    * `schema_list`: A package containing imported pydantic schemas

    **Yields**
    * (field_name, (field_type, ...)) where field name is the name of the
    field (string) associated with this relationship, and field_type is
    either the schema class if found (requires schema package to be set) or Any
    """
    mapper = inspect(ModelType)

    for relationship in mapper.relationships:
        # name of the attribute, will be returned
        field_name = relationship.key

        # pull the actual attribute from the class
        field = getattr(ModelType, field_name)

        # get the name of the tables for the other end of this relationship
        table_name = ""
        if field.expression.left.description == "id":
            table_name = field.expression.left.table.description
        elif field.expression.right.description == "id":
            table_name = field.expression.right.table.description

        # try to map other table name to a known schema if schema package is defined
        field_type = Any
        for cls in schema_list:
            if ins.isclass(cls) and cls.__name__.lower() == remove_endstr(
                table_name, "model"
            ):
                field_type = cls

        yield field_name, (field_type, ...)


def dict_relationship_attrs(
    ModelType: DeclarativeBase, schema_list: list[object] = []
) -> dict[str, tuple[type | Any | None, ...]]:
    """
    Dictionary that gives same values as gen_relationship_attrs

    **Parameters**

    See gen_relationship_attrs

    **Returns**

    dict generated from gen_relationship_attrs
    """

    output = {}
    for field_name, (field_type, _) in gen_relationship_attrs(ModelType, schema_list):
        output[field_name] = (field_type, ...)

    return output
