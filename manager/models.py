from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship
Base = declarative_base()
# from .crud import CRUD

class Users(Base):
    '''
    roles:
     * 0 - simple user - simple functions
     * 1 - moderator   - + moderator functions (delete, add products)
     * 2 - admin       - + admin functions (add moderators)
    '''
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    role = Column(Integer, default=0)  
    
class Basket(Base):
    '''
    many lines with one user id and different products id
    I/You can change this to one line for one user and json array with products id and quantity
    '''
    __tablename__ = "basket"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    products_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    photo = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    type_id = Column(Integer, ForeignKey("type.id"), nullable=True)

class Type(Base):
    __tablename__ = "type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

class TextContent(Base):
    __tablename__ = "texts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_en = Column(String, nullable=False)
    text_content = Column(Text, nullable=False)

    
if __name__ == "__main__":
    Product.create()