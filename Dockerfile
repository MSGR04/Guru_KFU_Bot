FROM python:3.9-slim

# Установка зависимостей
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бота
COPY . .

# Указываем команду запуска бота
CMD ["python", "bot.py"]