import telebot

API_TOKEN = "8739134919:AAH8csG0v-Y3MTHO6U_UREeq7byPy3LuNnM"
bot = telebot.TeleBot(API_TOKEN)

# 👑 админ
ADMIN_ID = 6498779131


# 🚀 старт
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎨 Заказать дизайн", "📞 Помощь")

    bot.send_message(message.chat.id, "Добро пожаловать в FAH DESIGNERS 👑", reply_markup=markup)


# 🎨 заказ
@bot.message_handler(func=lambda m: m.text == "🎨 Заказать дизайн")
def order(message):
    msg = bot.send_message(message.chat.id, "Опиши заказ:")
    bot.register_next_step_handler(msg, process_order)


def process_order(message):
    user = message.from_user
    username = f"@{user.username}" if user.username else "Без ника"

    text = f"""
📥 Новый ЗАКАЗ!

👤 Ник: {username}
🆔 ID: {user.id}

📝 Заказ:
{message.text}

👉 Ответить:
/reply {user.id} текст
"""

    bot.send_message(ADMIN_ID, text)
    bot.send_message(message.chat.id, "✅ Заказ отправлен!")


# 📞 помощь (ТЕПЕРЬ КАК ЗАКАЗ)
@bot.message_handler(func=lambda m: m.text == "📞 Помощь")
def help_request(message):
    msg = bot.send_message(message.chat.id, "Напиши свой вопрос:")
    bot.register_next_step_handler(msg, process_help)


def process_help(message):
    user = message.from_user
    username = f"@{user.username}" if user.username else "Без ника"

    text = f"""
📞 НОВОЕ ОБРАЩЕНИЕ!

👤 Ник: {username}
🆔 ID: {user.id}

💬 Сообщение:
{message.text}

👉 Ответить:
/reply {user.id} текст
"""

    bot.send_message(ADMIN_ID, text)
    bot.send_message(message.chat.id, "✅ Сообщение отправлено админу!")


# 💬 ответ админа
@bot.message_handler(commands=['reply'])
def reply_to_user(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        args = message.text.split(" ", 2)
        user_id = int(args[1])
        text = args[2]

        bot.send_message(user_id, f"💬 Ответ от администратора:\n\n{text}")
        bot.send_message(message.chat.id, "✅ Отправлено")

    except:
        bot.send_message(message.chat.id, "❌ Пример: /reply 123456789 текст")


# 🔥 запуск
bot.infinity_polling()
