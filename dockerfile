FROM python:3.13-slim

# Установим системные зависимости (если нужны для сборки)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Устанавливаем Poetry 2.1.2 напрямую
RUN curl -sSL https://install.python-poetry.org | python3 - --version 2.1.2 && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Копируем только файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем только прод-зависимости, без виртуального окружения
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копируем остальной код
COPY . .

# Переменные и порт
ENV PORT=8000
EXPOSE $PORT

# Запуск
CMD ["gunicorn", "src.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
