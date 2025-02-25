from os import getenv
from dotenv import load_dotenv

from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, Session
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer, BigInteger, DECIMAL
from sqlalchemy import create_engine, ForeignKey, UniqueConstraint

load_dotenv()

BD_USER = getenv('DB_USER')
BD_PASSWORD = getenv('DB_PASSWORD')
BD_ADDRESS = getenv('DB_ADDRESS')
BD_NAME = getenv('DB_NAME')

engine = create_engine(f'postgresql://{BD_USER}:{BD_PASSWORD}@{BD_ADDRESS}', echo=True)

class Base(DeclarativeBase):
    pass

class Users(Base):
    """База пользователей"""
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    telegram: Mapped[int] = mapped_column(BigInteger, unique=True)
    phone: Mapped[str] = mapped_column(String(30), nullable=True)
    
    carts: Mapped[int] = relationship('Carts', back_populates='user_cart')
    
    def __str__(self):
        return self.name
    
class Carts(Base):
    """Временная корзина покупателя, используется до кассы"""
    __tablename__= 'carts'
    id:Mapped[int] = mapped_column(primary_key=True)
    total_price: Mapped[DECIMAL] = mapped_column(DECIMAL(12,2),default=0)
    total_product: Mapped[int] = mapped_column(default=0)
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
    
    user_cart: Mapped[Users] = relationship(back_populates='carts')
    finally_id: Mapped[int] = relationship('Finally_carts', back_populates='user_cart')
    
    def __str__(self):
        return str(self.id)
    
class Finally_carts(Base):
    """Окончательная корзина пользователя, возле кассы"""
    __tablename__='finally_cart'
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(50))
    finally_price: Mapped[DECIMAL] = mapped_column(DECIMAL(12,2), default=0)
    quantity: Mapped[int]
    
    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.id'))
    user_cart: Mapped[Carts] = relationship(back_populates='finally_id')
    
    __table_args__ = (UniqueConstraint('cart_id', 'product_name'),)
    
    def __str__(self):
        return str(self.id)
    
class Categories(Base):
    """Категории продуктов"""
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String(20), unique=True)
    
    products: Mapped[int] = relationship('Products', back_populates='product_categories')
    
    def __str__(self):
        return self.category_name
    
class Products(Base):
    """Продукты"""
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(20), unique=True)
    description: Mapped[str]
    image: Mapped[str] = mapped_column(String(100))
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(12,2), default=0)
    
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    product_categories: Mapped[Categories] = relationship(back_populates='products')
    
    

def main():
    Base.metadata.create_all(engine)
    #print (BD_USER)
    categories = ('Лаваши', 'Донары', 'Хот-Доги', 'Десерты', 'Соусы')
    products = (
        (1, 'Мини Лаваш', 20000, 'Мясо, тесто, помидоры', 'media/lavhash/i.jpeg'),
        (1, 'Мини Говяжий', 22000, 'Мясо, тесто, помидоры', 'media/lavhash/i.jpeg'),
        (1, 'Мини с сыром', 24000, 'Мясо, тесто, помидоры', 'media/lavhash/i.jpeg'),
        (2, 'Гамбургер', 18000, 'Мясо, тесто, помидоры', 'media/lavhash/i.jpeg'),
        (2, 'Дамбургер', 22000, 'Мясо, тесто, помидоры', 'media/lavhash/i.jpeg'),
        (2, 'Чизбургер', 19000, 'Мясо, тесто, помидоры', 'media/lavhash/i.jpeg'),
        
    )
    with Session(engine) as session:
        for category in categories:
            query = Categories(category_name=category)
            session.add(query)
            session.commit()
            
        for product in products:
            query = Products(
                category_id = product[0],
                product_name = product[1],
                price = product[2],
                description = product[3],
                image = product[4]
            )
            session.add(query)
            session.commit()
            
if __name__ == "__main__":
    main()