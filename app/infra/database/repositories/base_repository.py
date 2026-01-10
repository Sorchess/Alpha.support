import logging

from pydantic import BaseModel
from sqlalchemy import select, delete, update
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import ObjectNotFoundException, ObjectAlreadyExistsException

logger = logging.getLogger(__name__)


class BaseRepository:
    model = None
    schema = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        result = result.scalars().all()
        return [self.schema.model_validate(instance) for instance in result]

    async def get_one_or_none(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        result = result.scalars().one_or_none()
        return self.schema.model_validate(result) if result else None

    async def get_one(self, **kwargs):
        stmt = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        try:
            result = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.schema.model_validate(result)

    async def get_model(self, **kwargs):
        stmt = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        try:
            result = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return result

    async def add(self, schema: BaseModel):
        model_instance = self.model(**schema.model_dump())
        self.session.add(model_instance)

        try:
            await self.session.commit()
            return self.schema.model_validate(model_instance)
        except IntegrityError:
            await self.session.rollback()
            raise ObjectAlreadyExistsException

    async def patch(self, column: str, value: any, **kwargs):
        stmt = update(self.model).filter_by(**kwargs).values({column: value})
        await self.session.execute(stmt)
        await self.session.commit()

    async def update(self, schema: BaseModel, **kwargs):
        stmt = (
            update(self.model)
            .filter_by(**kwargs)
            .values(**schema.model_dump(exclude_none=True))
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, **filters):
        stmt = delete(self.model).filter_by(**filters)
        await self.session.execute(stmt)
        await self.session.commit()
