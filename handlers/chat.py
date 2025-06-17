from aiogram import types, Dispatcher
from database.redis import find_pair, remove_pair, set_waiting
from aiogram.dispatcher import FSMContext

active_chats = {}

async def search_cmd(message: types.Message, state: FSMContext):
    uid = str(message.from_user.id)
    partner_id = await find_pair(uid)
    if partner_id:
        active_chats[uid] = partner_id
        active_chats[partner_id] = uid
        await message.bot.send_message(partner_id, "Собеседник найден! Напишите сообщение.")
        await message.answer("Собеседник найден! Напишите сообщение.")
    else:
        await set_waiting(uid)
        await message.answer("Ожидание собеседника...")

async def message_relay(message: types.Message):
    uid = str(message.from_user.id)
    partner_id = active_chats.get(uid)
    if partner_id:
        try:
            await message.bot.send_message(partner_id, message.text)
        except:
            await message.answer("Ошибка отправки.")

async def stop_cmd(message: types.Message):
    uid = str(message.from_user.id)
    partner_id = active_chats.pop(uid, None)
    if partner_id:
        active_chats.pop(partner_id, None)
        await message.bot.send_message(partner_id, "Собеседник покинул чат.")
    await message.answer("Чат завершён.")

def register(dp: Dispatcher):
    dp.register_message_handler(search_cmd, commands=['search'])
    dp.register_message_handler(stop_cmd, commands=['stop'])
    dp.register_message_handler(message_relay, content_types=types.ContentTypes.TEXT)
