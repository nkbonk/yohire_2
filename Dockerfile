FROM python:3.10-slim


# адаём рабочую директорию внутри контейнера
WORKDIR /app

# Копируем описания зависимостей
COPY requirements.txt ./

# Ставим нужные пакеты
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY . .

# Команда по умолчанию — запускаем Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]