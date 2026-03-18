import telebot

API_TOKEN = "8739134919:AAH8csG0v-Y3MTHO6U_UREeq7byPy3LuNnM"

bot = telebot.TeleBot(API_TOKEN)

# 👑 админы
ADMINS = [6498779131]

# 🎨 дизайнеры (очередь)
designers = [6498779131, 7299702298, 6034730945, 6498779131]

queue_index = 0


# 🚀 старт
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("🎨 Заказать дизайн")
    btn2 = telebot.types.KeyboardButton("📞 Помощь")
    markup.add(btn1, btn2)

    bot.send_message(message.chat.id, "Добро пожаловать в FAH DESIGNERS 👑", reply_markup=markup)


# 🎨 заказ
@bot.message_handler(func=lambda message: message.text == "🎨 Заказать дизайн")
def order(message):
    msg = bot.send_message(message.chat.id, "Опиши заказ:")
    bot.register_next_step_handler(msg, process_order)


def process_order(message):
    global queue_index

    designer_id = designers[queue_index]

    # отправка дизайнеру
    bot.send_message(designer_id, f"📥 Новый заказ:\n\n{message.text}\n\nОт: {message.from_user.id}")

    # ответ клиенту
    bot.send_message(message.chat.id, "✅ Заказ отправлен дизайнеру!")

    # следующий дизайнер
    queue_index += 1
    if queue_index >= len(designers):
        queue_index = 0


# 📞 помощь
@bot.message_handler(func=lambda message: message.text == "📞 Помощь")
def help_msg(message):
    bot.send_message(message.chat.id, "Напиши администратору: @fahdesing_bot")


# 🔁 эхо (на всякий)
@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.chat.id, "Выбери кнопку 👇")


# 🔥 запуск
bot.infinity_polling()
