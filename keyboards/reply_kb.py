from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup



def share_phone_button() -> ReplyKeyboardMarkup:
    """Кнопка для отправки контакта"""
    builder = ReplyKeyboardBuilder()
    builder.button(text = 'Отправить свой контакт ☎️', request_contact=True)
    return builder.as_markup(resize_keyboard=True)