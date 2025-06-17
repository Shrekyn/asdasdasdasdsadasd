import aioredis
from config import REDIS_URL

redis = aioredis.from_url(REDIS_URL, decode_responses=True)

async def set_waiting(user_id):
    await redis.sadd("waiting", user_id)

async def find_pair(user_id):
    partner = await redis.spop("waiting")
    if partner and partner != user_id:
        return partner
    else:
        await redis.sadd("waiting", user_id)
        return None

async def remove_pair(user_id):
    await redis.srem("waiting", user_id)

async def get_user_count():
    return await redis.dbsize()
