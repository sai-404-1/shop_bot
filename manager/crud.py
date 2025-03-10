from sqlalchemy.orm import Session

class CRUD:
    def __init__(self, model):
        self.model = model

    @classmethod
    def for_model(cls, model):
        """Фабричный метод для создания экземпляра CRUD с моделью"""
        return cls(model=model)
    
    def create(self, db: Session, **kwargs):
        """Создать объект модели"""
        obj = self.model(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        print(f"Create new object in {self.model.__tablename__}: {obj}")
        return obj

    def get(self, db: Session, **kwargs):
        """Получить объект с дополнительными параметрами фильтрации"""
        query = db.query(self.model)

        for key, value in kwargs.items():
            query = query.filter(getattr(self.model, key) == value)

        obj = query.all()
        return obj
    
    def all(self, db: Session):
        """Получить все объекты модели"""
        print(self.model)
        return db.query(self.model).all()
    
    def update(self, db: Session, model_id: int, **kwargs):
        """Обновить все поля модели"""
        obj = db.query(self.model).filter(self.model.id == model_id).first()
        if obj:
            for field, value in kwargs.items():
                setattr(obj, field, value)
            db.commit()
            db.refresh(obj)
            print(f"Was updated an object in {self.model.__tablename__} was updated: {obj}")
            return obj
        return None
    
    def delete(self, db: Session, model_id: int):
        """Удалить объект из таблциы"""
        obj = db.query(self.model).filter(self.model.id == model_id).first()
        if obj:
            db.delete(obj)
            db.commit()
            print(f"Object (id:{self.model.id}) was deleted from {self.model.__tablename__}: {obj}")
            return obj
        return None