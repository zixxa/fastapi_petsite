from typing import Union
from uuid import UUID

from sqlalchemy import update, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User


class UserDAL:
    __db_session: AsyncSession

    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session

    async def create_user(
            self, name: str, surname: str, email: str
    ) -> User:
        new_user = User(name=name, surname=surname, email=email)
        self.__db_session.add(new_user)
        await self.__db_session.flush()
        return new_user

    async def delete_user(self, user_id:UUID) -> Union[User,None]:
        query = update(User).\
            where(and_(User.user_id == user_id, User.is_active == True)).\
            values(is_active=False).\
            returning(User.user_id)
        res = await self.__db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def get_user_by_id(self, user_id:UUID) -> Union[User,None]:
        query = select(User).where(and_(User.user_id == user_id, User.is_active == True))
        res = await self.__db_session.execute(query)
        user = res.fetchone()
        if user is not None:
            return user[0]

    async def update(self):
        pass