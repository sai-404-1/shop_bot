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
        return obj

    def get(self, db: Session, model_id: int):
        """Получить объект по ID"""
        obj = db.query(self.model).filter(self.model.id == model_id).first()
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
            return obj
        return None
    
    def delete(self, db: Session, model_id: int):
        """Удалить объект из таблциы"""
        obj = db.query(self.model).filter(self.model.id == model_id).first()
        if obj:
            db.delete(obj)
            db.commit()
            return obj
        return None