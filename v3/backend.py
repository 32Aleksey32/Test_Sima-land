from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from hasher import get_password_hash, verify_password
from jose import JWTError, jwt
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data_base import Permission, User, engine

# чтобы получить строку, подобную этой, запустите: openssl rand -hex 32
SECRET_KEY = "5787ecd3040f4cf2fa97db4b97ea74d8"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_db():
    session = AsyncSession(engine)
    try:
        yield session
    finally:
        await session.close()


async def create_user(db: AsyncSession, user):
    new_user = User(first_name=user.first_name.capitalize(),
                    last_name=user.last_name.capitalize(),
                    login=user.login,
                    password=get_password_hash(user.password),
                    date_of_birth=user.date_of_birth)
    db.add(new_user)
    permission = Permission(readonly=user.login)
    db.add(permission)
    await db.commit()
    user = select(User).where(User.login == user.login)
    result = await db.execute(user)
    return result.scalars().first()


async def get_users(db: AsyncSession):
    users = select(User).order_by(User.id)
    result = await db.execute(users)
    return result.scalars().all()


async def update_user(db: AsyncSession, id, first_name,
                      last_name, date_of_birth, password):
    user = update(User).where(User.id == id)
    if first_name:
        user = user.values(first_name=first_name)
    if last_name:
        user = user.values(last_name=last_name)
    if password:
        user = user.values(password=password)
    if date_of_birth:
        user = user.values(date_of_birth=date_of_birth)
    user.execution_options(synchronize_session="fetch")
    await db.execute(user)
    await db.commit()


async def delete_user(db: AsyncSession, id):
    user = delete(User).where(User.id == id)
    await db.execute(user)
    permission = delete(Permission).where(Permission.id == id)
    await db.execute(permission)
    await db.commit()


async def get_user_by_id(db: AsyncSession, id):
    user = select(User).filter(User.id == id)
    result = await db.execute(user)
    return result.scalars().first()


async def get_user_by_login(db: AsyncSession, login):
    user = select(User).filter(User.login == login)
    result = await db.execute(user)
    return result.scalars().first()


async def authenticate_user(db: AsyncSession, login, password):
    user = await get_user_by_login(db, login)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(db: AsyncSession = Depends(get_db),
                           token=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_login(db, login=username)
    if user is None:
        raise credentials_exception
    return user


async def create_access_token(data: dict, expires_delta: Optional[timedelta]):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
