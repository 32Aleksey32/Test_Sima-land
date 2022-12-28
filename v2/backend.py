from sqlalchemy import delete, update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from data_base import Permission, User
from aiohttp import web

class User_CRUD:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_user(self, first_name, last_name,
                          login, password, date_of_birth):
        new_user = User(first_name=first_name, last_name=last_name,
                        login=login, password=password,
                        date_of_birth=date_of_birth)
        self.db_session.add(new_user)
        permission = Permission(readonly=login)
        self.db_session.add(permission)
        await self.db_session.commit()
        user = select(User).where(User.login == login)
        perform = await self.db_session.execute(user)
        return perform.scalars().first()

    async def get_users(self):
        users = select(User).order_by(User.id)
        perform = await self.db_session.execute(users)
        return perform.scalars().all()

    # async def get_users(self):
    #     users = select(User).order_by(User.id)
    #     perform = await self.db_session.execute(users)
    #     b = perform.scalars().all()
    #     a = {'ddd': 'aaa'}
    #     c = [a, b]
    #
    #     return c

    async def update_user(self, first_name, last_name,
                          login, password, date_of_birth):
        user = update(User).where(User.login == login)
        if first_name:
            user = user.values(first_name=first_name)
        if last_name:
            user = user.values(last_name=last_name)
        if password:
            user = user.values(password=password)
        if date_of_birth:
            user = user.values(date_of_birth=date_of_birth)
        user.execution_options(synchronize_session="fetch")
        await self.db_session.execute(user)
        await self.db_session.commit()
        user = select(User).where(User.login == login)
        perform = await self.db_session.execute(user)
        return perform.scalars().first()

    async def delete_user(self, login):
        user = delete(User).where(User.login == login)
        await self.db_session.execute(user)
        permission = delete(Permission).where(Permission.readonly == login)
        await self.db_session.execute(permission)
        await self.db_session.commit()
        return f'Пользователь {login} удален.'
