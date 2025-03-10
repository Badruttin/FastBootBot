from typing import Iterable

from sqlalchemy.orm import Session
from sqlalchemy import update, delete, select
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
    