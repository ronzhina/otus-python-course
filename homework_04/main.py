import asyncio
from typing import List

from loguru import logger
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession

from homework_04.jsonplaceholder_requests import fetch_users_data, fetch_posts_data
from homework_04.models import Base, engine, User, Post, Session

metadata = MetaData()


async def create_schemas():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def create_many_users(users: List[dict], session: AsyncSession):
    logger.info("create_many_users")
    for user in users:
        session.add(User(user['name'], user['username'], user['email']))
    await session.commit()


async def create_many_posts(posts: List[dict], session: AsyncSession):
    logger.info("create_many_posts")
    for post in posts:
        session.add(Post(post['userId'], post['title'], post['body']))
    await session.commit()


async def async_main():
    logger.info('async_main start')
    logger.info('creation DB start')
    await create_schemas()
    logger.info('creation DB finish')

    logger.info('get_users and get_posts start')
    users_data: List[dict]
    posts_data: List[dict]
    users_data, posts_data = await asyncio.gather(
        fetch_users_data(),
        fetch_posts_data())
    logger.info('get_users and get_posts finish')

    logger.info('create_many_users and create_many_posts start')
    async with Session() as session:
        await create_many_users(users_data, session)
        await create_many_posts(posts_data, session)
    logger.info('create_many_users and create_many_posts finish')

    logger.info('async_main finish')
    await engine.dispose()


def main():
    logger.info('main start')
    asyncio.run(async_main())
    logger.info('main finish')


if __name__ == "__main__":
    main()
