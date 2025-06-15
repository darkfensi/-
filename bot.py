import telebot
from telebot import types
from database import init_db, save_data, get_user_data, delete_data_by_id, find_best_match, is_admin, set_admin
from phash_utils import extract_icon_from_image, extract_features, compare_features_clip
from gdrive_utils import upload_to_gdrive
import os

BOT_TOKEN = "7611456298:AAG60fHiSCy0_QSuj8i9nAePsbEG6nrzj1U"
bot = telebot.TeleBot(BOT_TOKEN)
STATE = {}
init_db()

@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if is_admin(chat_id):
        markup.add("📤 Загрузить данные", "🔍 Получить данные", "📂 Мои данные", "🚪 Выход")
    else:
        markup.add("🔍 Получить данные")
    bot.send_message(chat_id, "Добро пожаловать!", reply_markup=markup)

@bot.message_handler(commands=['admin'])
def admin_handler(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введите пароль:")
    STATE[chat_id] = "awaiting_password"

@bot.message_handler(func=lambda message: STATE.get(message.chat.id) == "awaiting_password")
def check_password(message):
    if message.text == "SOVA754":
        set_admin(message.chat.id)
        bot.send_message(message.chat.id, "Админ режим активирован.")
    else:
        bot.send_message(message.chat.id, "Неверный пароль.")
    STATE.pop(message.chat.id, None)
    start_handler(message)

@bot.message_handler(func=lambda msg: msg.text == "📤 Загрузить данные")
def upload_data(msg):
    bot.send_message(msg.chat.id, "Отправьте иконку (фото):")
    STATE[msg.chat.id] = "awaiting_photo"

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    if STATE.get(chat_id) == "awaiting_photo":
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        os.makedirs("uploaded", exist_ok=True)
        filepath = f"uploaded/{file_info.file_unique_id}.jpg"
        with open(filepath, "wb") as f:
            f.write(downloaded_file)
        STATE[chat_id] = {"photo_path": filepath, "step": "awaiting_link"}
        bot.send_message(chat_id, "Теперь отправьте ссылку:")
    elif STATE.get(chat_id) == "search":
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        image_path = f"search/{file_info.file_unique_id}.jpg"
        os.makedirs("search", exist_ok=True)
        with open(image_path, "wb") as f:
            f.write(downloaded_file)
        icon = extract_icon_from_image(image_path)
        if not icon:
            bot.send_message(chat_id, "Иконка не найдена.")
            return
        features = extract_features(icon)
        match = find_best_match(features)
        if match:
            bot.send_message(chat_id, f"Найдена ссылка: {match[1]}")
        else:
            bot.send_message(chat_id, "Совпадений не найдено.")
        STATE.pop(chat_id, None)

@bot.message_handler(func=lambda message: isinstance(STATE.get(message.chat.id), dict) and STATE[message.chat.id].get("step") == "awaiting_link")
def handle_link(message):
    chat_id = message.chat.id
    photo_path = STATE[chat_id]["photo_path"]
    link = message.text
    features = extract_features(photo_path)
    gdrive_url = upload_to_gdrive(photo_path)
    save_data(photo_path, link, chat_id, features, gdrive_url)
    bot.send_message(chat_id, "Данные успешно сохранены.")
    STATE.pop(chat_id, None)

@bot.message_handler(func=lambda msg: msg.text == "🔍 Получить данные")
def get_data_handler(msg):
    chat_id = msg.chat.id
    STATE[chat_id] = "search"
    bot.send_message(chat_id, "Отправьте изображение:")

@bot.message_handler(func=lambda msg: msg.text == "📂 Мои данные")
def my_data_handler(msg):
    user_data = get_user_data(msg.chat.id)
    for item in user_data:
        file_id, path, link = item
        with open(path, "rb") as photo:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("❌ Удалить", callback_data=f"delete_{file_id}"))
            bot.send_photo(msg.chat.id, photo, caption=link, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_"))
def delete_handler(call):
    file_id = int(call.data.split("_")[1])
    delete_data_by_id(file_id)
    bot.answer_callback_query(call.id, "Удалено.")

@bot.message_handler(func=lambda msg: msg.text == "🚪 Выход")
def exit_admin(msg):
    chat_id = msg.chat.id
    set_admin(chat_id, False)
    bot.send_message(chat_id, "Вы вышли из админ-режима.")
    start_handler(msg)

bot.infinity_polling()