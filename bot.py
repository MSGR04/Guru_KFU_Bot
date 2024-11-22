import asyncio
import requests

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

TOKEN = '7608926069:AAHqWOz0V9dSlqqAyKNA02Y162C6ZgL5hfc'
ADMIN_SERVER_URL = 'https://gurukfuadminbot-production.up.railway.app/new_request'
user_data_storage = {}
ADMIN_ID = 866765016

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_storage[user_id] = {'started': True}  # Устанавливаем флаг, что пользователь начал сессию

    keyboard = [[InlineKeyboardButton("📑Курсовая работа — от 3500", callback_data='1'),
                InlineKeyboardButton(" 🧑‍🔬Научная работа — от 2000", callback_data='2')],
                [InlineKeyboardButton("🔬Д/З — индивидуально", callback_data='3'),
                InlineKeyboardButton("📋ЦОР — от 1000", callback_data='4')],
                [InlineKeyboardButton("📊Презентация — от 100", callback_data='5'),
                InlineKeyboardButton("🕵️Другое🕵", callback_data='other')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Как дела с учебой? Вернись к заданиям и попробуй решить их сам!\n\n"
        "Если у самого решить задания не получилось, то я тебя приветствую!👋\n\n"
        " ✨Я помогу облегчить твою студенческую жизнь✨\n"
        "Мы предлагаем услуги по написанию:\n"
        " • курсовых 📑\n"
        " • научных работ 🧑\n"
        " • домашних заданий 🔬\n"
        " • заданий в ЦОРе 📋\n"
        " • презентаций 📊\n"
        " • других работ 🕵️\n\n"
        "Указаны минимальные цены и могут меняться в зависимости от сложности и сроков выполнения.\n\n"
        "Познакомиться с нами подробнее и посмотреть отзывы можно [тут](https://www.youtube.com/watch?v=dQw4w9WgXcQ).",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    await asyncio.sleep(1.5)
    await update.message.reply_text(
        "С чем тебе помочь?",
        reply_markup=reply_markup,
    )

async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if user_id not in user_data_storage or (not user_data_storage[user_id].get('started')):
        await query.answer("Пожалуйста, сначала введите /start для начала работы с ботом.", show_alert=True)
        return

    await query.answer()
    if query.data == '1':
        user_data_storage[user_id]['type'] = 'Курсовая работа'
        await query.edit_message_text(
            "Введите отдельно в каждой строке следующую информацию:\n"
            "институт (КФУ, ИУЭиФ)\n"
            "направление (экономика (бух учёт));\n"
            "курс (3 курс);\n"
            "академическая группа;\n"
            "фамилию и инициалы руководителя, можно сокращенно;\n"
            "название темы;\n"
            "критерии (шрифт, размер, отступы, объём теории и практики, количество символов и т.д.) — просьба по критериям скидывать только необходимую информацию;\n"
            "дату сдачи (15.02.2025)."
        )
    elif query.data == '2':
        user_data_storage[user_id]['type'] = 'Научная работа'
        await query.edit_message_text(
            "Введите отдельно в каждой строке следующую информацию:\n"
            "институт (КФУ, ИУЭиФ)\n"
            "направление (экономика (бух учёт));\n"
            "курс (3 курс);\n"
            "академическая группа;\n"
            "фамилию и инициалы научного руководителя, можно сокращенно;\n"
            "название темы;\n"
            "критерии (шрифт, размер, отступы, название научного журнала, количество символов и т.д.) — просьба по критериям скидывать только необходимую информацию;\n"
            "дату сдачи (15.02.2025)."
        )
    elif query.data == '3':
        user_data_storage[user_id]['type'] = 'Д/З'
        await query.edit_message_text(
            "Опишите домашнее задание (фотография, скриншот, особенности задания, подробное описание), название предмета и обозначьте дату сдачи."
        )

    elif query.data == '4':
        user_data_storage[user_id]['type'] = 'ЦОР'
        await query.edit_message_text(
            "Введите отдельно в каждой строке следующую информацию:\n"
            "институт (КФУ, ИУЭиФ);\n"
            "направление (экономика (бух учёт));\n"
            "курс (3 курс);\n"
            "предмет (теория вероятности);\n"
            "дату сдачи (15.02.2025)."
        )

    elif query.data == '5':
        user_data_storage[user_id]['type'] = 'Презентация'
        await query.edit_message_text(
            "Введите отдельно в каждой строке следующую информацию:\n"
            "институт (КФУ, ИУЭиФ);\n"
            "направление (экономика (бух учёт));\n"
            "курс (3 курс);\n"
            "предмет (теория вероятности);\n"
            "Опишите критерии презентации, например: (презентация должна состоять на основе текста, количество слайдов, особенное оформление);\n"
            "дату сдачи (15.02.2025)."
        )

    elif query.data == 'other':
        user_data_storage[user_id]['type'] = 'Другое'
        await query.edit_message_text(
            "Подробно опишите с чем вам нужна помощь:"
        )


async def save_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_text = update.message.caption if update.message.caption else update.message.text  # Используем caption для фото
    has_photo = bool(update.message.photo)
    photo_url = None  # Ссылка на фото

    # Проверяем, что пользователь начал сессию и выбрал тип запроса
    if user_id not in user_data_storage or not user_data_storage[user_id].get('started'):
        await update.message.reply_text("Пожалуйста, сначала введите /start для начала работы с ботом.")
        return

    if 'type' in user_data_storage[user_id]:
        request_type = user_data_storage[user_id]['type']

        # Валидация формата данных для каждого типа запроса
        is_valid = False
        if request_type == 'Курсовая работа':
            is_valid = len(user_text.splitlines()) == 8
        elif request_type == 'Научная работа':
            is_valid = len(user_text.splitlines()) == 8
        elif request_type == 'Д/З':  # Домашнее задание
            is_valid = bool(user_text)  # Обязательное текстовое описание, фото необязательно
        elif request_type == 'ЦОР':
            is_valid = len(user_text.splitlines()) == 5
        elif request_type == 'Презентация':
            is_valid = len(user_text.splitlines()) >= 5
        elif request_type == 'Другое':
            is_valid = bool(user_text)

        if is_valid:
            # Если есть фото, получаем его URL
            if has_photo:
                file = await context.bot.get_file(update.message.photo[-1].file_id)
                photo_url = file.file_path

            # Отправляем запрос на сервер, включая URL фотографии
            requests.post(ADMIN_SERVER_URL, json={
                'user_id': user_id,
                'request_type': request_type,
                'details': user_text,
                'photo_url': photo_url  # Передаем URL фотографии
            })
            await update.message.reply_text(
                "Спасибо за Ваше доверие, мы приняли Ваш запрос! По всем дополнительным вопросам с Вами свяжется специалист в течение суток, ожидайте.")
            del user_data_storage[user_id]
        else:
            await update.message.reply_text("Введите данные в правильном формате")
    else:
        await update.message.reply_text("Пожалуйста, выберите услугу, прежде чем отправлять данные.")


if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_query))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_user_input))
    app.add_handler(MessageHandler(filters.PHOTO, save_user_input))
    app.run_polling()
