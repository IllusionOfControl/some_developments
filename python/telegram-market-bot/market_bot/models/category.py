from sqlalchemy import Column, String, Integer, Boolean
from market_bot.database.dbcore import Base


class Category(Base):
    """
    Класс-модель для описания таблицы "Категория товара",
    основан на декларативном стиле SQLAlchemy
    """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    is_active = Column(Boolean)

    def __repr__(self):
        """
        Метод возвращает формальное строковое представление указанного объекта
        """
        return self.name
