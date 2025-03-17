from aiogram.utils.keyboard import InlineKeyboardBuilder 
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_utils import db_get_all_category, db_get_products

def generate_category_menu() -> InlineKeyboardMarkup:
    """Кнопки категорий"""
    categories = db_get_all_category()
    builder = InlineKeyboardBuilder()
    # TODO общая сумма корзинки
    builder.button(text = f'Ваша корзинка (TODO руб.)', callback_data='Ваша корзинка')
    [builder.button(text = category.category_name, callback_data=f'category_{category.id}') for category in categories]
    builder.adjust(1,2)
    return builder.as_markup()

def show_product_by_category(category_id:int) -> InlineKeyboardMarkup:
    """Кнопки продуктов"""
    products = db_get_products(category_id)
    builder = InlineKeyboardBuilder()
    [builder.button(text=product.product_name,
                    callback_data=f'product_{product.id}') for product in products]
    builder.adjust(2)
    builder.row(
        InlineKeyboardButton(text='⬅Назад',
                             callback_data='return_to_category')
    )
    return builder.as_markup()