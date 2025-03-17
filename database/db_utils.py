from typing import Iterable

from sqlalchemy.orm import Session
from sqlalchemy import DECIMAL, update, delete, select
from sqlalchemy.sql.functions import sum
from sqlalchemy.exc import IntegrityError
from aiogram.utils.keyboard import ReplyKeyboardBuilder


from .models import Carts, Categories, Products, Finally_carts, Users, engine

with Session(engine) as session:
    db_session = session
    
def db_register_user(full_name: str, chat_id: int) -> bool:
    """Первая регистрация пользователя с доступными данными"""
    try:
        query = Users(name = full_name, telegram = chat_id)
        db_session.add(query)
        db_session.commit()
        return False
    except IntegrityError:
        db_session.rollback()
        return True
    
def db_update_user(chat_id: int, phone: str):
    """Добавление информации о номере телефона"""
    query = update(Users).where(Users.telegram == chat_id).values(phone=phone)
    db_session.execute(query)
    db_session.commit()
    
def db_create_user_cart(chat_id: int):
    """Создание временной корзинки пользователя"""
    try:
        subquery = db_session.scalar(select(Users).where(Users.telegram == chat_id))
        query = Carts(user_id = subquery.id)
        db_session.add(query)
        db_session.commit()
        return True
    except IntegrityError:
        """Если карта существует"""
        db_session.rollback()
    except AttributeError:
        """Если контакт отправил анонимный пользователь"""
        db_session.rollback()
        
def db_get_all_category() -> Iterable:
    """Получаем все категории """
    try:
        query = db_session.scalars(select(Categories))
        pass
    except IntegrityError:
        pass
    return query
    
def db_get_products(category_id) ->Iterable:
    """Получаем продукты категории по id"""
    query =  select(Products).where(Products.category_id == category_id)
    try:
        return db_session.scalars(query)
    except IntegrityError:
        db_session.rollback()
        
def db_get_product_by_id(product_id: int) -> Products:
    """Получаем из базы данные о продукте"""
    query = select(Products).where(Products.id == product_id)
    return db_session.scalar(query)

def db_get_user_cart(chat_id: int) -> Carts:
    """Получаем ID корзинки по таблице User"""
    query = select(Carts.id).join(Users).where(Users.telegram==chat_id)
    return db_session.scalar(query)

def db_update_to_cart(price: DECIMAL, cart_id: int, quantity=1) -> None:
    """Обновляем данные временной корзины"""
    query=update(Carts).where(Carts.id==cart_id
                              ).values(total_price = price,
                                       total_product=quantity)
    db_session.execute(query)
    db_session.commit()
    