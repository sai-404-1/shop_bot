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

    # Определяем модель с которой будем взаимодействовать
    model = Product

    # Заполнение товарами
    CRUD.for_model(Product).create(db_session, 
        name="iPhone 16 Nike Pro Max", 
        description="iPhone 16 Pro Max — флагманский смартфон от Apple с процессором A17 Bionic, 6,7-дюймовым дисплеем Super Retina XDR, улучшенной камерой, поддержкой 5G и длительным временем работы.", 
        price=1000, 
        photo="16pro.jpg", 
        type_id=1
    )
    CRUD.for_model(Product).create(db_session, 
        name="iPhone 10", 
        description="iPhone X — это революционный смартфон от Apple с безрамочным 5,8-дюймовым дисплеем Super Retina, процессором A11 Bionic, двойной камерой с режимом портрета и системой Face ID для разблокировки по лицу.", 
        price=600, 
        photo="10.jpg", 
        type_id=1
    )
    CRUD.for_model(Product).create(db_session, 
        name="Какой-то монстр", 
        description="Монстр в стекле", 
        price=666, 
        photo="mosnterEE015.png", 
        type_id=2
    )
    CRUD.for_model(Product).create(db_session, 
        name="Какой-то розовый монстр", 
        description="Монстр в банке", 
        price=666, 
        photo="mosnterUS05.png", 
        type_id=2
    )
    print("Products was created")

    # Заполнение типов
    CRUD.for_model(Type).create(db_session, 
        name="etc",
        newest=True,
        description="Тип для Монстров"
    )
    CRUD.for_model(Type).create(db_session, 
        name="ps",
        newest=True,
        description="Тип для PlayStation"
    )
    CRUD.for_model(Type).create(db_session, 
        name="xbox",
        newest=True,
        description="Тип для xbox"
    )
    CRUD.for_model(Type).create(db_session, 
        name="chargers", 
        newest=True,
        description="Тип для зарядных устройств"
    )
    CRUD.for_model(Type).create(db_session, 
        name="cases", 
        description="Тип для чехлов"
    )
    CRUD.for_model(Type).create(db_session, 
        name="glasses", 
        description="Тип для стёкол"
    )
    CRUD.for_model(Type).create(db_session, 
        name="speakers", 
        description="Тип для колонок"
    )

    CRUD.for_model(Type).create(db_session, 
        name="dyson_styler", 
        description="Тип для стайлера dyson"
    )
    CRUD.for_model(Type).create(db_session, 
        name="dyson_straightener", 
        description="Тип для выпрямителя dyson"
    )
    CRUD.for_model(Type).create(db_session, 
        name="dyson_hair_dryer", 
        description="Тип для фена dyson"
    )
    # б/у                             ================================================
    CRUD.for_model(Type).create(db_session, 
        name="used_iphone", 
        description="Тип для б/у iphone"
    )
    CRUD.for_model(Type).create(db_session, 
        name="used_android", 
        description="Тип для б/у android"
    )
    CRUD.for_model(Type).create(db_session, 
        name="used_tablets", 
        description="Тип для б/у планшетов"
    )
    CRUD.for_model(Type).create(db_session, 
        name="used_notebooks", 
        description="Тип для б/у ноутбуков"
    )
    CRUD.for_model(Type).create(db_session, 
        name="used_watches", 
        description="Тип для б/у часов"
    )
    CRUD.for_model(Type).create(db_session, 
        name="used_headphones", 
        description="Тип для б/у наушников"
    )
    CRUD.for_model(Type).create(db_session, 
        name="dyson_hair_dryer", 
        description="Тип для фена dyson"
    )

    # новые                             ================================================
    CRUD.for_model(Type).create(db_session, 
        name="apple",
        newest=True,
        description="Тип для iPhone"
    )
    CRUD.for_model(Type).create(db_session, 
        name="new_android", 
        description="Тип для новых android"
    )
    CRUD.for_model(Type).create(db_session, 
        name="new_tablets", 
        description="Тип для новых планшетов"
    )
    CRUD.for_model(Type).create(db_session, 
        name="new_notebooks", 
        description="Тип для новых ноутбуков"
    )
    CRUD.for_model(Type).create(db_session, 
        name="new_watches", 
        description="Тип для новых часов"
    )
    CRUD.for_model(Type).create(db_session, 
        name="new_headphones", 
        description="Тип для новых наушников"
    )
    print("Types was created")

    # Заполнение пользователей
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