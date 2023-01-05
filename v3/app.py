from datetime import timedelta

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm as OAuth2
from hasher import get_password_hash
from schemas import UserModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend import (authenticate_user, create_access_token, create_user,
                     delete_user, get_current_user, get_db, get_user_by_id,
                     get_users, update_user)
from data_base import User

routes = FastAPI()


@routes.get('/users')
async def get_all_users(db: AsyncSession = Depends(get_db)):
    func = await get_users(db)
    return func


@routes.post('/registration')
async def create_users(user: UserModel, db: AsyncSession = Depends(get_db)):
    try:
        call_func = await create_user(db, user)
        return call_func
    except IntegrityError:
        return "Такой логин уже используется, придумайте новый."


@routes.put('/update/{id}')
async def update_users(id: int, current_user: UserModel,
                       db: AsyncSession = Depends(get_db)):
    users = await get_user_by_id(db, id)
    if not users:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Пользователя с id {id} не существует")
    if users.id == users.id:
        await update_user(db, id, current_user.first_name.capitalize(),
                          current_user.last_name.capitalize(),
                          current_user.date_of_birth,
                          get_password_hash(current_user.password))
        return {"msg": "Пользователь Успешно изменен."}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Вам не разрешается!")


@routes.delete('/delete/{id}')
async def delete_users(id: int, db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    user = await get_user_by_id(db, id)
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Пользователя с id {id} не существует")
    if user.id == current_user.id:
        await delete_user(db, id)
        return {"msg": "Пользователь успешно удален."}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Вам не разрешается!")


@routes.post("/token")
async def login_for_access_token(db: AsyncSession = Depends(get_db),
                                 form_data: OAuth2 = Depends()):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильное имя пользователя или пароль")
    access_token_expires = timedelta(hours=24)
    access_token = await create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@routes.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


if __name__ == '__main__':
    uvicorn.run("app:routes", port=9090, host='localhost')
