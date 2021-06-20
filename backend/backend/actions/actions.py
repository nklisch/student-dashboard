from ..database.models import Repos
from ..schemas import Repo
from sqlalchemy.orm import Session
from ..database import SQLBase
from pydantic import BaseModel
from typing import TypeVar, List, Union

ModelType = TypeVar("ModelType", bound=SQLBase)
SchemaType = TypeVar("SchemaType", bound=BaseModel)

# GETS
def get_all(
    db: Session, filter_by: dict, model: ModelType, schema: SchemaType = None
) -> Union[List[ModelType], List[SchemaType]]:
    result = db.query(model).filter_by(**filter_by).all()
    if schema:
        return [schema.from_orm(m) for m in result]
    return result


def get(
    db: Session, filter_by: dict, model: ModelType, schema: SchemaType = None
) -> ModelType:
    return db.query(model).filter_by(**filter_by).one()


# CREATES
def create(db: Session, data: Union[dict, SchemaType], model: ModelType) -> ModelType:
    data_db = model(**convert_schema_to_dict(data))
    db.add(data_db)
    db.commit()
    db.refresh(data_db)
    return data_db


def create_or_update(
    db: Session, data: Union[dict, SchemaType], model: ModelType
) -> ModelType:
    data_db = model(**convert_schema_to_dict(data))
    db.merge(data_db)
    db.commit()
    db.refresh(data_db)
    return


def create_or_update_all(
    db: Session, data: Union[List[dict], List[SchemaType]], model: ModelType
):
    data = [model(**convert_schema_to_dict(d)) for d in data]
    # db.add_all(data)
    for d in data:
        db.merge(d)
    db.commit()


def convert_schema_to_dict(data):
    if type(data) is not dict:
        return data.dict()
    return data
