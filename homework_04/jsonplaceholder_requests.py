import aiohttp
import ujson as ujson
from aiohttp import TCPConnector
from loguru import logger

USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users/"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts/"


async def new_fetch_json(url):
    logger.info('Fetch url {}', url)
    async with aiohttp.ClientSession(json_serialize=ujson.dumps, connector=TCPConnector(verify_ssl=False)) as session:
        async with session.get(url) as resp:
            return await resp.json()


async def fetch_users_data():
    return await new_fetch_json(USERS_DATA_URL)


async def fetch_user_data(user_id):
    return await new_fetch_json(f'{USERS_DATA_URL}/{user_id}')


async def get_user_albums_data(user_id):
    return await new_fetch_json(f'{USERS_DATA_URL}/{user_id}/albums')


async def get_user_todos_data(user_id):
    return await new_fetch_json(f'{USERS_DATA_URL}/{user_id}/todos')


async def get_user_posts_data(user_id):
    return await new_fetch_json(f'{USERS_DATA_URL}/{user_id}/posts')


async def fetch_posts_data():
    return await new_fetch_json(POSTS_DATA_URL)


async def fetch_post_data(post_id):
    return await new_fetch_json(f'{POSTS_DATA_URL}/{post_id}')


async def fetch_post_comments_data(post_id):
    return await new_fetch_json(f'{POSTS_DATA_URL}/{post_id}/comments')
