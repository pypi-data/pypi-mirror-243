from pydantic import create_model, BaseModel
from pydantic.main import ModelMetaclass
from typing import Generic, TypeVar
from instarest.db.base_class import DeclarativeBase
from instarest.utils.models import (
    dict_column_attrs_with_id,
    dict_optional_column_attrs_no_id,
    dict_relationship_attrs,
    remove_endstr,
)

ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class SchemaBase(Generic[ModelType]):
    def __init__(
        self,
        model: type[ModelType] = DeclarativeBase,
        include_relationship_schemas: list[BaseModel | ModelMetaclass] = [],
        optional_fields: list[str] = [],
    ):
        """
        Wrapper class for pydantic schemas needed to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class that inherits from DeclarativeBase.  Defaults to DeclarativeBase.
        * `include_relationship_schemas`: list of pydantic schemas that should be included in the
        http response whose underlying SQLAlchemy models have a relationship.  Defaults to empty.
        """

        assert issubclass(model, DeclarativeBase)

        # DO NOT REORDER
        self.model = model
        self.include_relationship_schemas = include_relationship_schemas
        self.optional_fields = optional_fields
        self.EntityBase = self._build_entity_base()
        self.EntityCreate = self._build_entity_create()
        self.EntityUpdate = self._build_entity_update()
        self.EntityInDBBase = self._build_entity_in_db_base()
        self.Entity = self._build_entity()
        self.EntityInDB = self._build_entity_in_db()
        # DO NOT REORDER

    def get_model_type(self):
        return self.model

    def get_schema_prefix(self):
        return remove_endstr(self.model.__name__, "Model")

    # shared properties
    def _build_entity_base(self):
        class Config:
            arbitrary_types_allowed = True

        fields, validators = dict_optional_column_attrs_no_id(self.model)
        return create_model(
            f"{self.get_schema_prefix()}Base",
            __config__=Config,
            __validators__=validators,
            **fields,
        )

    # Properties to receive on Entity creation
    def _build_entity_create(self):
        return create_model(
            f"{self.get_schema_prefix()}Create", __base__=self.EntityBase
        )

    # Properties to receive on Entity update
    def _build_entity_update(self):
        return create_model(
            f"{self.get_schema_prefix()}Update", __base__=self.EntityBase
        )

    # Properties shared by models stored in DB
    def _build_entity_in_db_base(self):
        fields, _ = dict_column_attrs_with_id(
            self.model, optional_fields=self.optional_fields
        )

        # NOTES:
        # (1) separate __base__ and __config__ because pydantic
        # enforces only one at a time for clarity
        # (2) don't need to include validators because they are
        # already included in EntityBase
        db_base_schema = create_model(
            f"{self.get_schema_prefix()}InDBBase",
            __base__=self.EntityBase,
            **fields,
        )

        class EntityInDBBase(db_base_schema):
            class Config(db_base_schema.Config):
                orm_mode = True
                arbitrary_types_allowed = True

        return EntityInDBBase

    # Properties to return to client
    def _build_entity(self):
        return create_model(
            f"{self.get_schema_prefix()}",
            __base__=self.EntityInDBBase,
            **dict_relationship_attrs(self.model, self.include_relationship_schemas),
        )

    # Properties properties stored in DB
    def _build_entity_in_db(self):
        return create_model(
            f"{self.get_schema_prefix()}InDB", __base__=self.EntityInDBBase
        )
