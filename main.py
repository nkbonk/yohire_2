from dotenv import load_dotenv
import os

load_dotenv()  # ищет файл .env в корне проекта

POSTGRES_USER = os.getenv("POSTGRES_USER")         # имя пользователя PostgreSQL
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD") # пароль от БД
DATABASE_HOST = os.getenv("DATABASE_HOST")         # хост (обычно localhost)
DATABASE_PORT = os.getenv("DATABASE_PORT")         # порт (обычно 5432)
DATABASE_NAME = os.getenv("DATABASE_NAME")         # имя БД (например, yohire)

# Формируем URL для SQLAlchemy
DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:"
    f"{POSTGRES_PASSWORD}@"
    f"{DATABASE_HOST}:"
    f"{DATABASE_PORT}/"
    f"{DATABASE_NAME}"
)


from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Создаём движок SQLAlchemy — echo=True для логов SQL-запросов
engine = create_engine(DATABASE_URL, echo=True)

# Фабрика сессий для работы с БД:
#    autocommit=False — без commit() данные не сохраняются;
#    autoflush=False — без flush() изменения не синхронизируются автоматически;
#    bind=engine — привязываем к нашему движку
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Импортируем Base из моделей и создаём таблицы, которых ещё нет
from models import Base
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Роут для health-check: GET /
@app.get("/")
async def read_root():
    """
    Проверка: возвращаем простое сообщение,
    чтобы убедиться, что сервер запустился.
    """
    return {"message": "Yohire backend is up with .env!"}