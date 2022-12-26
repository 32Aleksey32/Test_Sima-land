from aiohttp import web
from sqlalchemy import exc, select

from data_base import Permission, User, async_session
from utils import logger

routes = web.RouteTableDef()


@routes.post('/create')
async def create_user(request):
    first_name = input('Введите имя для создания: ').capitalize()
    last_name = input('Введите фамилию для создания: ').capitalize()
    login = input('Введите логин для создания: ')
    password = input('Введите пароль для создания: ')
    date_of_birth = input('Введите дату рождения для создания: ')
    permission = input('Введите права: ')

    async with async_session() as session:
        async with session.begin():
            session.add(
                User(first_name=first_name,
                     last_name=last_name,
                     login=login,
                     password=password,
                     date_of_birth=date_of_birth,
                     permission=permission)
            )
            user = f'Имя: {first_name}, Фамилия: {last_name}, ' \
                   f'Логин: {login}, Дата рождения: {date_of_birth}, ' \
                   f'Права: {permission}'
            try:
                await session.commit()
                logger.info(f'Пользователь {login} успешно создан.')
                return web.Response(text=f'Создан пользователь:\n {user}')
            except exc.IntegrityError:
                msg = 'Проверьте правильность ввода или заполнение всех полей'
                logger.error(msg)
                return web.Response(text=msg)


@routes.get('/')
async def get_user(request):
    async with async_session() as session:
        users = await session.execute(select(User))
        data = []
        for user in users:
            data.append(f'Имя: {user[0].first_name}, '
                        f'Фамилия: {user[0].last_name}, '
                        f'Логин: {user[0].login}, '
                        f'Дата рождения: {user[0].date_of_birth}, '
                        f'Права: {user[0].permission}')
        results = '\n'.join(data)
        logger.info('Данные из таблиц у Вас на экране.')
        return web.Response(text=results)


# @routes.put('/put')
# async def put_user(request):
#     # data = postgres_db.update_user()
#     # return web.Response(text=data)
#     with Session(autoflush=False, bind=engine) as db:
#         login = input('Введите логин для редактирования: ')
#         per = input('Введите новые права для пользователя: ')
#         user = db.query(User).filter(User.login == login).first()
#         permission = db.query(Permission).filter(
#             Permission.permission == per).first()
#         if (user is not None) and (permission is not None):
#             user.permission_table = permission
#             db.commit()
#             logger.info(f'Пользователь {login} теперь имеет права {per}.')
#         return web.Response(text=f'У пользователя {login} были изменены права на {permission}')


@routes.delete('/delete')
async def delete_user(request):
    async with async_session() as session:
        login = input('Введите логин для удаления: ')
        select_db = select(User).where(User.login == login)
        users = await session.execute(select_db)
        for user in users:
            await session.delete(user[0])
        await session.commit()
        msg = f'Пользователь {login} удален.'
        logger.info(msg)
        return web.Response(text=msg)
        # else:
        #     error = f'Пользователя {login} не существует.'
        #     logger.error(error)
        #     return web.Response(text=error)


@routes.delete('/delete_permission')
async def delete_permission(request):
    async with async_session() as session:
        data = input('Введите права для удаления: ')
        select_db = select(Permission).where(Permission.permission == data)
        permissions = await session.execute(select_db)
        for permission in permissions:
            await session.delete(permission[0])
        await session.commit()
        msg = f'Права {data} удалены.'
        logger.info(msg)
        return web.Response(text=msg)
        # else:
        #     error = f'Таких прав как {permission} не существует.'
        #     logger.error(error)
        #     return web.Response(text=error)


app = web.Application()
app.add_routes(routes)
web.run_app(app, port=9090)
