FROM ultralytics/ultralytics:latest-python

WORKDIR /app

# Устанавливаем Poetry 2.1.2 напрямую
RUN pip install fastapi=0.115.12 uvicorn=0.34.1 gunicorn=23.0.0 omegaconf=2.3.0 websockets=15.0.1
# Копируем остальной код
COPY . .

# Переменные и порт
ENV PORT=8000
EXPOSE $PORT

# Запуск
CMD ["sh", "-c", "gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT"]
