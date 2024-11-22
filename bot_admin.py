from flask import Flask, request
from telegram import Bot
import asyncio
import requests
from io import BytesIO
import threading

app = Flask(__name__)
hyodsd
# Настройки бота-администратора
ADMIN_BOT_TOKEN = '7798675687:AAHKJ1FnY2t1J7xtmVnAipfa1xeMB4ylUqc'
ADMIN_CHAT_ID =  866765016 # Ваш Telegram ID или ID чата, куда будут приходить уведомления
admin_bot = Bot(token=ADMIN_BOT_TOKEN)

# Создаем отдельный event loop для асинхронных задач
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


# Запускаем event loop в отдельном потоке
def start_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()


threading.Thread(target=start_loop, daemon=True).start()


async def send_admin_message(message, photo_url=None):
    if photo_url:
        # Загрузка фото с URL и отправка его администратору
        photo_data = requests.get(photo_url).content
        await admin_bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=BytesIO(photo_data), caption=message)
    else:
        # Отправляем только текст, если фото нет
        await admin_bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)


@app.route('/new_request', methods=['POST'])
def new_request():
    data = request.json
    user_id = data.get('user_id')
    request_type = data.get('request_type')
    details = data.get('details')
    photo_url = data.get('photo_url')

    # Формируем сообщение
    message = (f"Новый запрос от пользователя {user_id}:\n"
               f"Тип запроса: {request_type}\n"
               f"Данные: {details}")

    # Запускаем асинхронную задачу в созданном event loop
    asyncio.run_coroutine_threadsafe(send_admin_message(message, photo_url), loop)

    return "OK", 200


if __name__ == '__main__':
    app.run(port=5001)
