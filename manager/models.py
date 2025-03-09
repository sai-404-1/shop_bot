from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
Base = declarative_base()
# from .crud import CRUD

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    type_id = Column(Integer, ForeignKey("type.id"), nullable=True)  # Внешний ключ

class Type(Base):
    __tablename__ = "type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

class TextContent(Base):
    __tablename__ = "texts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_en = Column(String, nullable=False)
    text_content = Column(Text, nullable=False)


if __name__ == "__main__":
    Product.create()