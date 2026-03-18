import telebot
from telebot import types

API_TOKEN = "8739134919:AAH8csG0v-Y3MTHO6U_UREeq7byPy3LuNnM"
bot = telebot.TeleBot(API_TOKEN)

ADMIN_ID = 6498779131

reply_dict = {}

# 🚀 старт
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎨 Заказать дизайн")
    markup.add("📞 Помощь", "🖼 Наши работы")

    bot.send_message(message.chat.id, "Добро пожаловать в FAH DESIGNERS 👑", reply_markup=markup)


# 🎨 заказ
@bot.message_handler(func=lambda m: m.text == "🎨 Заказать дизайн")
def order(message):
    msg = bot.send_message(message.chat.id, "Опиши заказ:")
    bot.register_next_step_handler(msg, process_order)


def process_order(message):
    user = message.from_user
    username = f"@{user.username}" if user.username else "Без ника"

    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("💬 Ответить", callback_data=f"reply_{user.id}")
    markup.add(btn)

    text = f"""
📥 Новый ЗАКАЗ!

👤 Ник: {username}
🆔 ID: {user.id}

📝 Заказ:
{message.text}
"""

    bot.send_message(ADMIN_ID, text, reply_markup=markup)
    bot.send_message(message.chat.id, "✅ Заказ отправлен!")


# 📞 помощь
@bot.message_handler(func=lambda m: m.text == "📞 Помощь")
def help_request(message):
    msg = bot.send_message(message.chat.id, "Напиши свой вопрос:")
    bot.register_next_step_handler(msg, process_help)


def process_help(message):
    user = message.from_user
    username = f"@{user.username}" if user.username else "Без ника"

    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("💬 Ответить", callback_data=f"reply_{user.id}")
    markup.add(btn)

    text = f"""
📞 НОВОЕ ОБРАЩЕНИЕ!

👤 Ник: {username}
🆔 ID: {user.id}

💬 Сообщение:
{message.text}
"""

    bot.send_message(ADMIN_ID, text, reply_markup=markup)
    bot.send_message(message.chat.id, "✅ Сообщение отправлено!")


# 🖼 наши работы (ПОКА ПУСТО)
@bot.message_handler(func=lambda m: m.text == "🖼 Наши работы")
def portfolio(message):
    bot.send_message(message.chat.id, "Скоро добавим работы 🔥")


# 🔘 кнопка "Ответить"
@bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
def callback_reply(call):
    if call.from_user.id != ADMIN_ID:
        return

    user_id = int(call.data.split("_")[1])
    reply_dict[call.from_user.id] = user_id

    bot.send_message(call.from_user.id, "✍️ Напиши ответ пользователю:")


# 💬 отправка ответа
@bot.message_handler(func=lambda message: message.from_user.id in reply_dict)
def send_reply(message):
    user_id = reply_dict[message.from_user.id]

    bot.send_message(user_id, f"💬 Ответ от администратора:\n\n{message.text}")
    bot.send_message(message.chat.id, "✅ Ответ отправлен")

    del reply_dict[message.from_user.id]


# 🔥 ЛОВИМ PHOTO ID
@bot.message_handler(content_types=['photo'])
def get_photo_id(message):
    file_id = message.photo[-1].file_id
    bot.send_message(message.chat.id, f"ID фото:\n{file_id}")


# 🚀 запуск
bot.infinity_polling()
