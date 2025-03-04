import sqlite3

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None
        self.cursor = None

        self._connect()

    def _connect(self):
        """Подключение к базе данных SQLite"""
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as err:
            print(f"Error connecting to database: {err}")
            exit(1)

    def create_tables(self):
        """Создание таблиц в базе данных"""
        categories_table = """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
        """
        
        products_table = """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL
        );
        """
        
        texts_table = """
        CREATE TABLE IF NOT EXISTS texts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_en TEXT NOT NULL,
            text_content TEXT NOT NULL
        );
        """
        
        try:
            self.cursor.execute(categories_table)
            self.cursor.execute(products_table)
            self.cursor.execute(texts_table)
            self.connection.commit()
            print("Tables created successfully.")
        except sqlite3.Error as err:
            print(f"Error creating tables: {err}")
            exit(1)

    def insert_category(self, name):
        """Добавление категории"""
        try:
            self.cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
            self.connection.commit()
            print(f"Category '{name}' added successfully.")
        except sqlite3.Error as err:
            print(f"Error inserting category: {err}")

    def insert_product(self, name, description, price):
        """Добавление товара"""
        try:
            self.cursor.execute("INSERT INTO products (name, description, price) VALUES (?, ?, ?)", 
                                (name, description, price))
            self.connection.commit()
            print(f"Product '{name}' added successfully.")
        except sqlite3.Error as err:
            print(f"Error inserting product: {err}")

    def insert_text(self, name_en, text_content):
        """Добавление текста"""
        try:
            self.cursor.execute("INSERT INTO texts (name_en, text_content) VALUES (?, ?)", 
                                (name_en, text_content))
            self.connection.commit()
            print(f"Text '{name_en}' added successfully.")
        except sqlite3.Error as err:
            print(f"Error inserting text: {err}")

    def update_category(self, category_id, new_name):
        """Обновление категории по id"""
        try:
            self.cursor.execute("UPDATE categories SET name = ? WHERE id = ?", (new_name, category_id))
            self.connection.commit()
            print(f"Category with ID {category_id} updated to '{new_name}'.")
        except sqlite3.Error as err:
            print(f"Error updating category: {err}")

    def update_product(self, product_id, new_name, new_description, new_price):
        """Обновление товара по id"""
        try:
            self.cursor.execute("UPDATE products SET name = ?, description = ?, price = ? WHERE id = ?", 
                                (new_name, new_description, new_price, product_id))
            self.connection.commit()
            print(f"Product with ID {product_id} updated.")
        except sqlite3.Error as err:
            print(f"Error updating product: {err}")

    def update_text(self, text_id, new_name_en, new_text_content):
        """Обновление текста по id"""
        try:
            self.cursor.execute("UPDATE texts SET name_en = ?, text_content = ? WHERE id = ?", 
                                (new_name_en, new_text_content, text_id))
            self.connection.commit()
            print(f"Text with ID {text_id} updated.")
        except sqlite3.Error as err:
            print(f"Error updating text: {err}")

    def delete_category(self, category_id):
        """Удаление категории по id"""
        try:
            self.cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
            self.connection.commit()
            print(f"Category with ID {category_id} deleted.")
        except sqlite3.Error as err:
            print(f"Error deleting category: {err}")

    def delete_product(self, product_id):
        """Удаление товара по id"""
        try:
            self.cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            self.connection.commit()
            print(f"Product with ID {product_id} deleted.")
        except sqlite3.Error as err:
            print(f"Error deleting product: {err}")

    def delete_text(self, text_id):
        """Удаление текста по id"""
        try:
            self.cursor.execute("DELETE FROM texts WHERE id = ?", (text_id,))
            self.connection.commit()
            print(f"Text with ID {text_id} deleted.")
        except sqlite3.Error as err:
            print(f"Error deleting text: {err}")

    def close(self):
        """Закрытие соединения с базой данных"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

if __name__ == "__main__":
    # Example usage
    db = Database(db_file='database.db')
    db.create_tables()

    # Insert some data
    db.insert_category('Electronics')
    db.insert_product('Laptop', 'High-performance laptop', 1200.99)
    db.insert_text('welcome_message', 'Welcome to our store!')

    # Update some data
    db.update_category(1, 'Updated Electronics')
    db.update_product(1, 'Gaming Laptop', 'Super fast gaming laptop', 1500.00)

    # Delete some data
    db.delete_category(1)
    db.delete_product(1)

    db.close()