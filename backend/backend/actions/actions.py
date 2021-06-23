from ..database.models import Repos
from ..schemas.db_schemas import Repo
from sqlalchemy.orm import Session
from ..database import SQLBase
from pydantic import BaseModel
from typing import TypeVar, List, Union
from ..schemas.requests import RequestConfig

ModelType = TypeVar("ModelType", bound=SQLBase)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class Action:
    def __init__(self, db: Session, model: ModelType, request_config: RequestConfig):
        self.model = model
        self.db = db

    def get_all(
        self,
        filter_by: dict = {},
        schema: SchemaType = None,
    ) -> Union[List[ModelType], List[SchemaType]]:
        result = (
            self.db.query(self.model)
            .filter_by(**filter_by)
            .offset(self.request_config.skip)
            .limit(self.request_config.limit)
            .all()
        )
        if schema:
            return [schema.from_orm(m) for m in result]
        return result

    def get(
        self,
        filter_by: dict = {},
        schema: SchemaType = None,
    ) -> Union[ModelType, SchemaType]:
        result = self.db.query(self.model).filter_by(**filter_by).one_or_none()
        if schema:
            return schema.from_orm(result)
        return result

    # CREATES
    def create(data: Union[dict, SchemaType]) -> ModelType:
        db = self.db
        data_db = self.convert_data_to_model(data)
        db.add(data_db)
        db.commit()
        db.refresh(data_db)
        return self, data_db

    def create_all(self, data: Union[dict, SchemaType]):
        db = self.db
        data = [self.convert_data_to_model(d) for d in data]
        db.add_all(data)
        db.commit()
        return self

    def create_or_update(self, data: Union[dict, SchemaType]) -> ModelType:
        db = self.db
        data_db = self.convert_data_to_model(data)
        db.merge(data_db)
        db.commit()
        return self

    def create_or_update_all(self, data: Union[List[dict], List[SchemaType]]):
        db = self.db
        data = [self.convert_data_to_model(d) for d in data]
        for d in data:
            db.merge(d)
        db.commit()
        return self

    def convert_schema_to_dict(self, data) -> dict:
        if type(data) is not dict:
            return data.dict()
        return data

    def convert_data_to_model(self, data: Union[dict, SchemaType]) -> ModelType:
        d = {
            k: v for k, v in self.convert_schema_to_dict(data).items() if v is not None
        }
        return self.model(**d)


# UPDATES
