import uvicorn
from fastapi import FastAPI

from backend import User_CRUD
from data_base import async_session

routes = FastAPI()


@routes.get('/users')
async def get_user():
    async with async_session() as session:
        async with session.begin():
            user_crud = User_CRUD(session)
            func = await user_crud.get_users()
            return func


@routes.post('/users')
async def create_user():
    async with async_session() as session:
        login = input('Введите логин для создания'
                      ' (редактировать его в дальнейшем нельзя): ')
        first_name = input('Введите имя для создания: ').capitalize()
        last_name = input('Введите фамилию для создания: ').capitalize()
        password = input('Введите пароль для создания: ')
        date_of_birth = input('Введите дату рождения для создания: ')
        user_crud = User_CRUD(session)
        func = await user_crud.create_user(first_name, last_name, login,
                                           password, date_of_birth)
        return func


@routes.put('/users')
async def update_user():
    async with async_session() as session:
        login = input('Введите логин чтобы начать редактирование: ')
        first_name = input('Введите новое имя: ').capitalize()
        last_name = input('Введите новую фамилию: ').capitalize()
        password = input('Введите введите новый пароль: ')
        date_of_birth = input('Введите новую дату рождения: ')
        user_crud = User_CRUD(session)
        func = await user_crud.update_user(first_name, last_name, login,
                                           password, date_of_birth)
        return func


@routes.delete('/users')
async def delete_user():
    async with async_session() as session:
        login = input('Введите логин чтобы удалить: ')
        user_crud = User_CRUD(session)
        func = await user_crud.delete_user(login)
        return func


if __name__ == '__main__':
    uvicorn.run("app:routes", port=9090, host='localhost')
