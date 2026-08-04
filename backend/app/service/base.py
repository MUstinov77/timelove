from typing import Any, TypeVar

from fastapi import HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.model.base import Base


ModelType = TypeVar("ModelType", bound=Base)

class BaseService:

    model: ModelType = None

    def __init__(self, session):
        self.session: AsyncSession = session

    async def create(self, values: dict):
        try:
            record = self.model(**values)
            self.session.add(record)
            await self.session.commit()
            return record
        except SQLAlchemyError:
            await self.session.rollback()
            raise HTTPException(400, "Error while creating instance")

    async def update(self, values: dict, obj_id: int):
        query = (
            update(self.model).
            where(self.model.id == obj_id).
            values(**values).
            returning(self.model)
        )
        result = await self.session.execute(query)
        return result.scalars().one()

    async def delete(self, obj_id: int):
        query = delete(self.model).where(self.model.id == obj_id).returning(self.model)
        result = await self.session.execute(query)
        return result.scalars().one()

    async def retrieve_one(self, field: Any, field_value: Any, *args, **kwargs):
        query = select(self.model).where(field == field_value)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def retrieve_one_by_id(self, obj_id: int):
        record = await self.retrieve_one(self.model.id, obj_id)
        return record

    async def retrieve_all(self, field: Any, field_value: Any):
        query = select(self.model).where(field == field_value)
        result = await self.session.execute(query)
        return result.scalars().all()


    async def update_instance(self, values: dict, obj_id :int):
        try:
            record = await self.update(values, obj_id)
            await self.session.commit()
            return record
        except SQLAlchemyError:
            await self.session.rollback()
            raise HTTPException(
                status_code=400,
                detail="Error while updating instance"
            )