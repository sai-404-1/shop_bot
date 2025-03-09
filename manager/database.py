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