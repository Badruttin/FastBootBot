from aiogram.utils.keyboard import InlineKeyboardBuilder 
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_utils import db_get_all_category

def generate_category_menu() -> InlineKeyboardBuilder:
    """Кнопки категорий"""
    categories = db_get_all_category()
    builder = InlineKeyboardBuilder()
    # TODO общая сумма корзинки
    builder.button(text = f'Ваша корзинка (TODO руб.)', callback_data='Ваша корзинка')
    
    
