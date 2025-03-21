from starter import *
import os

db_session = Database('database.db').Session()
try:

    yes_answer = ['yes', 'y', '1']
    answer = input(f"If u continue, database should be destroyed and restore from scratch. Continue?\n{yes_answer}: ")
    if answer in yes_answer:
        os.remove('src/database.db')
        print('Database was restore')
    else:
        print('This look like denial')
        exit()

    # Заполнение типов
    CRUD.for_model(Type).create(db_session, 
        name="etc",
        title="Другое",
        description="Тип для Монстров"
    )
    CRUD.for_model(Type).create(db_session, 
        name="ps",
        title="PlayStation",
        description="Тип для PlayStation"
    )
    CRUD.for_model(Type).create(db_session, 
        name="xbox",
        title="X-Box",
        description="Тип для xbox"
    )
    CRUD.for_model(Type).create(db_session, 
        name="chargers", 
        title="Зарядные устройства",
        description="Тип для зарядных устройств"
    )
    CRUD.for_model(Type).create(db_session, 
        name="cases", 
        title="Чехлы",
        description="Тип для чехлов"
    )
    CRUD.for_model(Type).create(db_session, 
        name="glasses", 
        title="Стекла",
        description="Тип для стёкол"
    )
    CRUD.for_model(Type).create(db_session, 
        name="speakers", 
        title="Колонки",
        description="Тип для колонок"
    )

    CRUD.for_model(Type).create(db_session, 
        name="dyson_styler", 
        title="Стайлер Dyson",
        description="Тип для стайлера dyson"
    )
    CRUD.for_model(Type).create(db_session, 
        name="dyson_straightener", 
        title="Выпрямитель Dyson",
        description="Тип для выпрямителя dyson"
    )
    CRUD.for_model(Type).create(db_session, 
        name="dyson_hair_dryer", 
        title="Фен Dyson",
        description="Тип для фена dyson"
    )
    # б/у ================================================
    CRUD.for_model(Type).create(db_session, 
        name="used_iphone", 
        title="Б/у iPhone",
        description="Тип для б/у iphone"
    )
    CRUD.for_model(Type).create(db_session, 
        name="used_android", 
        title="Б/у Android",
        description="Тип для б/у android"
    )
    CRUD.for_model(Type).create(db_session, 
        name="used_tablets", 
        title="Б/у Планшеты",
        description="Тип для б/у планшетов"
    )
    CRUD.for_model(Type).create(db_session, 
        name="used_notebooks", 
        title="Б/у Ноутбуки",
        description="Тип для б/у ноутбуков"
    )
    CRUD.for_model(Type).create(db_session, 
        name="used_watches", 
        title="Б/у Часы",
        description="Тип для б/у часов"
    )
    CRUD.for_model(Type).create(db_session, 
        name="used_headphones", 
        title="Б/у Наушники",
        description="Тип для б/у наушников"
    )
    CRUD.for_model(Type).create(db_session, 
        name="dyson_hair_dryer", 
        title="Фен Dyson",
        description="Тип для фена dyson"
    )

    # новые ================================================
    CRUD.for_model(Type).create(db_session, 
        name="new_iphone",
        title="новый iPhone",
        description="Тип для iPhone"
    )
    CRUD.for_model(Type).create(db_session, 
        name="new_android", 
        title="Новые Android",
        description="Тип для новых android"
    )
    CRUD.for_model(Type).create(db_session, 
        name="new_tablets", 
        title="Новые Планшеты",
        description="Тип для новых планшетов"
    )
    CRUD.for_model(Type).create(db_session, 
        name="new_notebooks", 
        title="Новые Ноутбуки",
        description="Тип для новых ноутбуков"
    )
    CRUD.for_model(Type).create(db_session, 
        name="new_watches", 
        title="Новые Часы",
        description="Тип для новых часов"
    )
    CRUD.for_model(Type).create(db_session, 
        name="new_headphones", 
        title="Новые Наушники",
        description="Тип для новых наушников"
    )

    # Заполнение товарами
    CRUD.for_model(Product).create(db_session, 
        name="iPhone 16 Nike Pro Max", 
        description="iPhone 16 Pro Max — флагманский смартфон от Apple с процессором A17 Bionic, 6,7-дюймовым дисплеем Super Retina XDR, улучшенной камерой, поддержкой 5G и длительным временем работы.", 
        price=1000, 
        photo="16pro.jpg", 
        type_id=18
    )
    CRUD.for_model(Product).create(db_session, 
        name="iPhone 10", 
        description="iPhone X — это революционный смартфон от Apple с безрамочным 5,8-дюймовым дисплеем Super Retina, процессором A11 Bionic, двойной камерой с режимом портрета и системой Face ID для разблокировки по лицу.", 
        price=600, 
        photo="10.jpg", 
        type_id=11
    )
    CRUD.for_model(Product).create(db_session, 
        name="Какой-то монстр", 
        description="Монстр в стекле", 
        price=666, 
        photo="mosnterEE015.png", 
        type_id=1
    )
    CRUD.for_model(Product).create(db_session, 
        name="Какой-то розовый монстр", 
        description="Монстр в банке", 
        price=666, 
        photo="mosnterUS05.png", 
        type_id=1
    )
    print("Products was created")

    CRUD.for_model(Users).create(db_session,
        user_id=5139311660,
        username="sai_404_1",
        role=1
    )
 
    CRUD.for_model(Users).create(db_session,
        user_id=7594389667,
        username="niko_404_1",
        role=0
    )
    print("Users was created")


    print("\n\nMove new file to the src/* (now i doesn't have time)")
    exit()

except Exception as e:
    print(f"Error: {e}")