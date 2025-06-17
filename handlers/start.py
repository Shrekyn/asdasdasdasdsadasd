from aiogram import types, Dispatcher
from config import CHANNEL_USERNAME, ADMIN_IDS
from utils.subscription import check_subscription

async def start_cmd(message: types.Message):
    if not await check_subscription(message.from_user.id):
        await message.answer(f"Пожалуйста, подпишись на канал {CHANNEL_USERNAME} чтобы пользоваться ботом.")
        return
    await message.answer("Добро пожаловать! Нажми /search для поиска собеседника.")

async def stats_cmd(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    from database.redis import get_user_count
    count = await get_user_count()
    await message.answer(f"Всего пользователей: {count}")

def register(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=['start'])
    dp.register_message_handler(stats_cmd, commands=['stats'])
