from dotenv import load_dotenv
import os

load_dotenv()  # после этого os.getenv сможет достать наши креды

# Формируем строку подключения к PostgreSQL из .env
DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('DATABASE_HOST')}:"
    f"{os.getenv('DATABASE_PORT')}/"
    f"{os.getenv('DATABASE_NAME')}"
)

# Подключаем SQLAlchemy и настраиваем движок и сессии
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Импортируем ORM-модель Vacancy и Base для миграции
from models import Vacancy, Base

# Создаем движок SQLAlchemy: echo=True выводит SQL-запросы в логах
engine = create_engine(DATABASE_URL, echo=True)
# Настраиваем фабрику сессий:
#    autocommit=False — без явного commit() изменений не будет;
#    autoflush=False — без flush() SQLAlchemy не синхронизирует изменения;
#    bind=engine — привязываем к нашему движку
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Проверяю, что таблица vacancies существует: создаем её, если нету её
Base.metadata.create_all(bind=engine)


def populate_test_data():
    """
    Функция заполняет таблицу Vacancy тестовыми данными.
    """
    # Открываем сессию для БД
    session = SessionLocal()

    try:
        # Готовим список тестовых вакансий
        fake_vacancies = [
            Vacancy(
                title="Junior Python Developer",
                description="Ищем начинающего Python-разработчика для стартапа."
            ),
            Vacancy(
                title="Middle Backend Engineer",
                description="Нужен опытный бэкендщик: FastAPI, PostgreSQL, Docker."
            ),
            Vacancy(
                title="Senior Data Scientist",
                description="Аналитика, машинное обучение, опыт с большими данными."
            ),
        ]

        # Добавляем все вакансии в сессию
        session.add_all(fake_vacancies)
        # Сохраняем изменения в базу
        session.commit()
        print(f"Inserted {len(fake_vacancies)} test vacancies.")

    except Exception as e:
        # При ошибке откатываем транзакцию
        session.rollback()
        print("Error inserting test data:", e)
        raise

    finally:
        # Закрываем сессию
        session.close()


# Запускаем функцию, если скрипт выполняется напрямую
if __name__ == "__main__":
    populate_test_data()