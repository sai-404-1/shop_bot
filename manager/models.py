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

    # Users methods
    def user_exists(self, user_id: int) -> bool:
        """
        check if user exists
        """
        with self.Session as session:
            user = session.query(Users).filter(Users.id == user_id).first()
            return not user is None

    def add_user(self, user_id: int, username: str):
        """
        add new user
        """
        with self.Session as session:
            user = Users(id=user_id, username=username)
            session.add(user)
    
    def get_username(self, user_id: int) -> str:
        """
        get username of user by id
        """
        with self.Session as session:
            user = session.query(Users).filter(Users.id == user_id).first()
            return user.username if not user is None else None    

    def get_role(self, user_id: int) -> int:
        """
        get role of user by id
        """	
        with self.Session as session:
            user = session.query(Users).filter(Users.id == user_id).first()
            return user.role if not user is None else -1
    
    def set_role(self, user_id: int, new_role: int) -> bool:
        """
        set role of user by id
        """
        with self.Session as session:
            user = session.query(Users).filter(Users.id == user_id).first()
            if not user is None:
                user.role = new_role
                session.commit()
                return True
            return False

    # Basket methods
    def add_basket_position(user_id: int, product_id: int, quantity: int):
        """
        add/change position in basket
        """
        with self.Session as session:
            basket_position = session.query(Basket).filter(Basket.user_id == user_id, Basket.product_id == product_id).first()
            if basket_position is None:
                basket_position = Basket(user_id=user_id, product_id=product_id, quantity=quantity)
                session.add(basket_position)
            else:
                basket_position.quantity = quantity
                session.commit()
        
    def get_all_basket_positions(user_id: int) -> list:
        """
        get all positions in basket
        returnable type: list<list<int>>
        returnable name of types: [[product_id, quantity]]
        """
        with self.Session as session:
            user_basket_positions = session.query(Basket).filter(Basket.user_id == user_id).all()
            user_basket_positions = [[basket_position.product_id, basket_position.quantity] for basket_position in user_basket_positions]
            return user_basket_positions if not user_basket_positions is None else []



if __name__ == "__main__":
    Product.create()