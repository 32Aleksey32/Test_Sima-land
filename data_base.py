import asyncio
import os

import asyncpg
import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from utils import logger

load_dotenv()

Base = declarative_base()

postgres_database = f"postgresql+asyncpg://{os.getenv('USER')}:" \
                    f"{os.getenv('PASSWORD')}@{os.getenv('HOST')}:" \
                    f"{os.getenv('PORT')}/{os.getenv('NAME')}"

engine = create_async_engine(postgres_database)
async_session = sessionmaker(engine, AsyncSession, expire_on_commit=False)


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    permission = Column(String, unique=True, nullable=False)
    user_table = relationship(
        "User",
        back_populates="permission_table",
        cascade="all, delete-orphan"
    )


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    login = Column(String(20), nullable=False, unique=True)
    password = Column(String(20), nullable=False)
    # date_of_birth = Column(Date, nullable=False)
    date_of_birth = Column(String, nullable=False)
    permission = Column(
        String,
        ForeignKey("permissions.permission"),
        nullable=False
    )
    permission_table = relationship("Permission", back_populates="user_table")


# Создание базы данных
def create_db():
    connection = psycopg2.connect(user=f"{os.getenv('USER')}",
                                  password=f"{os.getenv('PASSWORD')}")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute(f"create database {os.getenv('NAME')}")
    cursor.close()
    connection.close()
    logger.info(f'База данных создана')


# Создание таблиц в базе данных
async def create_tables():
    async with engine.begin() as conn:
        db = await conn.run_sync(Base.metadata.create_all)
        logger.info("Таблицы в базе данных созданы.")
        return db


# Заполнение базы данных по умолчанию
async def filling_tables(async_session):
    async with async_session() as session:
        async with session.begin():
            session.add_all(
                [
                    Permission(permission="administrator"),
                    Permission(permission="blocking"),
                    Permission(permission="readonly"),
                ]
            )
            session.add(
                User(first_name="admin",
                     last_name="admin",
                     login="admin",
                     password="admin",
                     date_of_birth='01-01-1970',
                     permission='administrator')
            )
            await session.commit()
            logger.info('Пользователь "админ" успешно создан.')


async def main():
    create_db()
    await create_tables()
    await filling_tables(async_session)
    await engine.dispose()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    # asyncio.run(main())
