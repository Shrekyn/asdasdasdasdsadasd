from aiogram import Bot
from config import CHANNEL_USERNAME

async def check_subscription(user_id):
    from main import bot
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False
