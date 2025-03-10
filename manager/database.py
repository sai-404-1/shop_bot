from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import *

class Database:
    def __init__(self, db_file):
        self.engine = create_engine(f"sqlite:///{db_file}", echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def insert_type(self, name):
        """Добавление товара"""
        with self.Session() as session:
            type = Type(name=name)
            session.add(type)
            session.commit()
            print(f"'{name}' added successfully.")

    def insert_product(self, name, description, price, type_id):
        """Добавление товара"""
        with self.Session() as session:
            product = Product(name=name, description=description, price=price, type_id=type_id)
            session.add(product)
            session.commit()
            print(f"Product '{name}' added successfully.")

    def get_products(self, where=None, equals=None):
        with self.Session() as session:
            if where != None:
                return session.query(Product).filter(getattr(Product, where) == equals).all()
            return session.query(Product).all()

    def update_product(self, product_id, new_name, new_description, new_price):
        """Обновление товара"""
        with self.Session() as session:
            product = session.get(Product, product_id)
            if product:
                product.name = new_name
                product.description = new_description
                product.price = new_price
                session.commit()
                print(f"Product with ID {product_id} updated.")
            else:
                print(f"Product with ID {product_id} not found.")

    def delete_product(self, product_id):
        """Удаление товара"""
        with self.Session() as session:
            product = session.get(Product, product_id)
            if product:
                session.delete(product)
                session.commit()
                print(f"Product with ID {product_id} deleted.")
            else:
                print(f"Product with ID {product_id} not found.")



    def insert_text(self, name_en, text_content):
        """Добавление текста"""
        with self.Session() as session:
            text = TextContent(name_en=name_en, text_content=text_content)
            session.add(text)
            session.commit()
            print(f"Text '{name_en}' added successfully.")

    def update_text(self, text_id, new_name_en, new_text_content):
        """Обновление текста"""
        with self.Session() as session:
            text = session.get(TextContent, text_id)
            if text:
                text.name_en = new_name_en
                text.text_content = new_text_content
                session.commit()
                print(f"Text with ID {text_id} updated.")
            else:
                print(f"Text with ID {text_id} not found.")

    def delete_text(self, text_id):
        """Удаление текста"""
        with self.Session() as session:
            text = session.get(TextContent, text_id)
            if text:
                session.delete(text)
                session.commit()
                print(f"Text with ID {text_id} deleted.")
            else:
                print(f"Text with ID {text_id} not found.")

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
    # Example usage
    db = Database(db_file='database.db')
    # db.create_tables()

    # Insert some data
    # db.insert_category('Electronics')
    # for entity in db.get_categorys():
    #     print(entity.id, entity.name)

    # db.insert_type('ДАЙСОН НАШИ ЛЮБИМЫЕ МУА <3 СУКА ОБОЖАЮ ИХ САМЫЕ ЛУЧШИЕ')
    # db.insert_product('Сварщики dyson со всем перечнем товара', 'Вы когда-нибудь видели такое?', 1000.00, 1)
    # for entity in db.get_products():
    #     print(entity.id, entity.name, entity.description, entity.price, entity.type_id)

    # db.close()