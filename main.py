import asyncio
from os import getenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from keyboards.inline_kb import *
from keyboards.reply_kb import *
from database.db_utils import *

from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

load_dotenv()

TOKEN = getenv('TOKEN')
dp = Dispatcher()
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

@dp.message(CommandStart())
async def command_start(message: Message):
    """Старт бота"""
    await message.answer(f'Здравствуйте, <i> {message.from_user.full_name}</i>,\n'
                         f'Вас приветствует бот')
    await register_start_user(message)
    
async def register_start_user(message: Message):
    """Первая регистрация пользователя, с проверкой на существование"""
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    if db_register_user(full_name, chat_id):
        await message.answer(text = 'Авторизация прошла успешно')
        await show_main_menu(message)
    else:
        await message.answer(text = 'Для связи с Вами нам необходим контактный номер телефона', reply_markup=share_phone_button())

@dp.message(F.contact)
async def update_user_info_finish_register(message: Message):
    """Обновление данных пользователя его контактом"""
    chat_id = message.chat.id
    phone = message.contact.phone_number
    db_update_user(chat_id, phone)
    if db_create_user_cart(chat_id):
        await message.answer(text='Регистрация прошла успешно')
    await show_main_menu(message)
    
async def show_main_menu(message: Message):
    """Сделать заказ, История, Корзинка, Настройки"""
    await message.answer(text='Выберите направление',
                         reply_markup=generate_main_menu())


@dp.message(F.text == '🍩 Сделать заказ')
async def make_order(message: Message):
    """Реакция на кнопку Сделать заказ"""
    chat_id = message.chat.id
    # TODO Получить id корзины пользователя
    await bot.send_message(chat_id=chat_id,
                           text = 'Погнали',
                           reply_markup=back_to_main_menu())
    await message.answer(text = 'Выберите категорию', reply_markup='')


async def main():
    await dp.start_polling(bot)
    
if __name__=='__main__':
    asyncio.run(main())