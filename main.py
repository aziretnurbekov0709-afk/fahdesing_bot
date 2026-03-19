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

# 🖼 превью работы
PREVIEW_WORKS = [
    ("AgACAgIAAxkBAAMDabw93Fkfq06aZ3DKUCEdfeE19poAAnYRaxsfquBJ5gZiOfgmIMsBAAMCAAN5AAM6BA", "🔥 Превью 1"),
    ("AgACAgIAAxkBAAMCabw93J8px8B9VfJFVZRF3DFuu6cAAnURaxsfquBJIDvM2r0pjhQBAAMCAAN5AAM6BA", "🔥 Превью 2"),
    ("AgACAgIAAxkBAAMEabw93Feo6etfWkHJ6fMkm1j3f6AAAncRaxsfquBJ2231ax8S070BAAMCAAN5AAM6BA", "🔥 Превью 3"),
    ("AgACAgIAAxkBAAMFabw93KWdwnPMZ3Sh5IDyGOQ5dmkAAnkRaxsfquBJm_qNCstY7mMBAAMCAAN5AAM6BA", "🔥 Превью 4"),
    ("AgACAgIAAxkBAAMGabw93MXy01Jke3bSC8Q7fQpOUq0AAnoRaxsfquBJNbr08s0QFMoBAAMCAAN5AAM6BA", "🔥 Превью 5"),
    ("AgACAgIAAxkBAAMHabw93EJzduLx1R67BfkDu8SDwcoAAnsRaxsfquBJFGHgkKueF3sBAAMCAAN5AAM6BA", "🔥 Превью 6"),
]


# 🚀 старт
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("🎨 Заказать дизайн")
    markup.add("🤖 Бот / Сайт / Игра", "🎬 ИИ Видео / Монтаж")
    markup.add("🎥 Превью YouTube", "🖼 Работы превью")
    markup.add("🪪 Визитка / Карточка")

    bot.send_message(message.chat.id, "FAH DESIGNERS 👑", reply_markup=markup)


# 📤 функция отправки заказа
def send_order(message, target_id, category):
    user = message.from_user
    username = f"@{user.username}" if user.username else "Без ника"

    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("💬 Ответить", callback_data=f"reply_{user.id}")
    markup.add(btn)

    bot.send_message(target_id, f"""
📥 Новый заказ ({category})

👤 {username}
🆔 {user.id}

📝 {message.text}
""", reply_markup=markup)

    bot.send_message(message.chat.id, "✅ Заказ отправлен!")


# 🎨 обычный дизайн → тебе
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


# 🖼 работы превью
@bot.message_handler(func=lambda m: m.text == "🖼 Работы превью")
def preview_works(message):
    for file_id, text in PREVIEW_WORKS:
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("🎥 Заказать такое", callback_data="order_preview")
        markup.add(btn)

        bot.send_photo(message.chat.id, file_id, caption=text, reply_markup=markup)


# заказ с превью
@bot.callback_query_handler(func=lambda call: call.data == "order_preview")
def order_preview(call):
    msg = bot.send_message(call.message.chat.id, "✍️ Напиши детали:")
    bot.register_next_step_handler(msg, lambda m: send_order(m, PREVIEW_ADMIN, "Превью"))


# 💬 ответ
@bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
def reply(call):
    user_id = int(call.data.split("_")[1])
    reply_dict[call.from_user.id] = user_id
    bot.send_message(call.from_user.id, "Напиши ответ:")


@bot.message_handler(func=lambda m: m.from_user.id in reply_dict)
def send_reply(message):
    user_id = reply_dict[message.from_user.id]

    bot.send_message(user_id, f"💬 Ответ:\n{message.text}")
    bot.send_message(message.chat.id, "✅ Отправлено")

    del reply_dict[message.from_user.id]


# 🚀 запуск
bot.infinity_polling()
