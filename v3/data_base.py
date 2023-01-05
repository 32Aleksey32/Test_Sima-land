import asyncio
import os

import psycopg2
from dotenv import load_dotenv
from hasher import get_password_hash
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

Base = declarative_base()

DATABASE_URL = f"postgresql+asyncpg://{os.getenv('USER')}:" \
                    f"{os.getenv('PASSWORD')}@{os.getenv('HOST')}:" \
                    f"{os.getenv('PORT')}/{os.getenv('NAME')}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, AsyncSession, expire_on_commit=False)


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    administrator = Column(String)
    readonly = Column(String)
    blocking = Column(String)
    # users = relationship("User", back_populates="permissions")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    login = Column(String(20), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    date_of_birth = Column(String, nullable=False)
    # permissions = relationship("Permission", back_populates="users")


# Создание базы данных
def create_db():
    connection = psycopg2.connect(user=f"{os.getenv('USER')}",
                                  password=f"{os.getenv('PASSWORD')}")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute(f"create database {os.getenv('NAME')}")
    cursor.close()
    connection.close()


# Создание таблиц в базе данных
async def create_tables():
    async with engine.begin() as conn:
        db = await conn.run_sync(Base.metadata.create_all)
        return db


# Заполнение базы данных по умолчанию
async def filling_tables(async_session):
    async with async_session() as session:
        async with session.begin():
            session.add(
                User(first_name="admin",
                     last_name="admin",
                     login="admin",
                     password=get_password_hash("admin"),
                     date_of_birth='01-01-1970')
            )
            session.add(Permission(administrator="admin"))
            await session.commit()


async def main():
    create_db()
    await create_tables()
    await filling_tables(async_session)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
