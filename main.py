import telebot
from telebot import types

API_TOKEN = "8739134919:AAH8csG0v-Y3MTHO6U_UREeq7byPy3LuNnM"
bot = telebot.TeleBot(API_TOKEN)

# 👑 главный
ADMIN_ID = 6498779131

# 👨‍🎨 исполнители
PREVIEW_ADMIN = 7299702298
VIDEO_ADMIN = 6034730945

reply_dict = {}
orders = {}
reviews_wait = {}

# 🖼 ОБЩИЕ РАБОТЫ
WORKS = [
    ("AgACAgIAAxkBAAIBA2m6_cw-2NWOdv9-himqbG36O9FlAALqFmsbf4jQSUtF5w_1LyAEAQADAgADeQADOgQ", "🔥 Дизайн 1"),
    ("AgACAgIAAxkBAAIBBWm6_czZu0w68bV1MyHgWxB7Kk66AAJBG2sbV4LZSeER3otALILhAQADAgADeQADOgQ", "🔥 Дизайн 2"),
]

# 🎥 ПРЕВЬЮ РАБОТЫ
PREVIEW_WORKS = [
    ("AgACAgIAAxkBAAMDabw93Fkfq06aZ3DKUCEdfeE19poAAnYRaxsfquBJ5gZiOfgmIMsBAAMCAAN5AAM6BA", "🔥 Превью 1"),
    ("AgACAgIAAxkBAAMCabw93J8px8B9VfJFVZRF3DFuu6cAAnURaxsfquBJIDvM2r0pjhQBAAMCAAN5AAM6BA", "🔥 Превью 2"),
]


# 🚀 СТАРТ
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("🎨 Заказать дизайн")
    markup.add("🤖 Бот / Сайт / Игра", "🎬 ИИ Видео / Монтаж")
    markup.add("🎥 Превью YouTube", "🖼 Работы превью")
    markup.add("🪪 Визитка / Карточка")
    markup.add("🖼 Наши работы")
    markup.add("📊 Статус заказа", "⭐ Отзыв")

    bot.send_message(message.chat.id, "FAH DESIGNERS 👑", reply_markup=markup)


# 📤 ОТПРАВКА ЗАКАЗА
def send_order(message, target_id, category):
    user = message.from_user
    username = f"@{user.username}" if user.username else "Без ника"

    orders[user.id] = "⏳ В ожидании"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💬 Ответить", callback_data=f"reply_{user.id}"))

    bot.send_message(target_id, f"""
📥 Новый заказ ({category})

👤 {username}
🆔 {user.id}

📝 {message.text}

📊 Статус: ⏳ В ожидании
""", reply_markup=markup)

    bot.send_message(message.chat.id, "✅ Заказ отправлен!")


# 🎨 ДИЗАЙН → тебе
@bot.message_handler(func=lambda m: m.text == "🎨 Заказать дизайн")
def design(message):
    msg = bot.send_message(message.chat.id, "Опиши дизайн:")
    bot.register_next_step_handler(msg, lambda m: send_order(m, ADMIN_ID, "Дизайн"))


# 🤖 → тебе
@bot.message_handler(func=lambda m: m.text == "🤖 Бот / Сайт / Игра")
def bot_site(message):
    msg = bot.send_message(message.chat.id, "Опиши проект:")
    bot.register_next_step_handler(msg, lambda m: send_order(m, ADMIN_ID, "Бот/Сайт/Игра"))


# 🎬 → монтажеру
@bot.message_handler(func=lambda m: m.text == "🎬 ИИ Видео / Монтаж")
def video(message):
    msg = bot.send_message(message.chat.id, "Опиши монтаж:")
    bot.register_next_step_handler(msg, lambda m: send_order(m, VIDEO_ADMIN, "Монтаж"))


# 🎥 → превью дизайнеру
@bot.message_handler(func=lambda m: m.text == "🎥 Превью YouTube")
def preview(message):
    msg = bot.send_message(message.chat.id, "Опиши превью:")
    bot.register_next_step_handler(msg, lambda m: send_order(m, PREVIEW_ADMIN, "Превью"))


# 🪪 → тебе
@bot.message_handler(func=lambda m: m.text == "🪪 Визитка / Карточка")
def card(message):
    msg = bot.send_message(message.chat.id, "Опиши визитку:")
    bot.register_next_step_handler(msg, lambda m: send_order(m, ADMIN_ID, "Визитка"))


# 🖼 ОБЩИЕ РАБОТЫ
@bot.message_handler(func=lambda m: m.text == "🖼 Наши работы")
def works(message):
    for file_id, text in WORKS:
        bot.send_photo(message.chat.id, file_id, caption=text)


# 🎥 ПРЕВЬЮ РАБОТЫ
@bot.message_handler(func=lambda m: m.text == "🖼 Работы превью")
def preview_works(message):
    for file_id, text in PREVIEW_WORKS:
        bot.send_photo(message.chat.id, file_id, caption=text)


# 📊 СТАТУС
@bot.message_handler(func=lambda m: m.text == "📊 Статус заказа")
def status(message):
    st = orders.get(message.from_user.id, "❌ Нет заказа")
    bot.send_message(message.chat.id, f"📊 Статус:\n{st}")


# ⭐ ОТЗЫВ
@bot.message_handler(func=lambda m: m.text == "⭐ Отзыв")
def review(message):
    reviews_wait[message.from_user.id] = True
    bot.send_message(message.chat.id, "Напиши отзыв:")


@bot.message_handler(func=lambda m: m.from_user.id in reviews_wait)
def save_review(message):
    bot.send_message(ADMIN_ID, f"⭐ Отзыв:\n{message.text}")
    bot.send_message(message.chat.id, "Спасибо ❤️")
    del reviews_wait[message.from_user.id]


# 💬 ОТВЕТ
@bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
def reply(call):
    user_id = int(call.data.split("_")[1])
    reply_dict[call.from_user.id] = user_id
    bot.send_message(call.from_user.id, "Напиши ответ:")


@bot.message_handler(func=lambda m: m.from_user.id in reply_dict)
def send_reply(message):
    user_id = reply_dict[message.from_user.id]
    bot.send_message(user_id, f"💬 Админ:\n{message.text}")
    del reply_dict[message.from_user.id]


# 🚀 ЗАПУСК
bot.infinity_polling()
