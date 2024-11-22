# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы бота в контейнер
COPY .. .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Команда для запуска бота
CMD ["python", "bot_admin.py"]