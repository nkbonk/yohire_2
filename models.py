from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# формат табличечки
from sqlalchemy import Column, Integer, String, Text

class Vacancy(Base):
    """
    ORM-модель для таблицы вакансий:
    каждая строка – одна вакансия.
    """
    __tablename__ = "vacancies"  # имя таблицы в базе

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(255),
        nullable=False,
        index=True
    )

    description = Column(
        Text,
        nullable=False
    )