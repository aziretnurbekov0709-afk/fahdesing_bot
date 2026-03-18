import telebot
from telebot import types

API_TOKEN = "8739134919:AAH8csG0v-Y3MTHO6U_UREeq7byPy3LuNnM"
bot = telebot.TeleBot(API_TOKEN)

ADMIN_ID = 6498779131

reply_dict = {}
waiting_payment = {}
orders = {}
reviews_wait = {}

CARD_NUMBER = "4196720050644946"
CARD_NAME = "NURBOLOT DUISHENBAI UULU"


# 🖼 работы
WORKS = [
    ("AgACAgIAAxkBAAIBA2m6_cw-2NWOdv9-himqbG36O9FlAALqFmsbf4jQSUtF5w_1LyAEAQADAgADeQADOgQ", "🔥 Дизайн\n💰 1000₽"),
]


# 🚀 старт
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎨 Заказать дизайн")
    markup.add("📊 Статус заказа", "⭐ Отзыв")
    markup.add("🖼 Наши работы", "💳 Оплатить")

    bot.send_message(message.chat.id, "FAH DESIGNERS 👑", reply_markup=markup)


# 🎨 заказ
@bot.message_handler(func=lambda m: m.text == "🎨 Заказать дизайн")
def order(message):
    msg = bot.send_message(message.chat.id, "Опиши заказ:")
    bot.register_next_step_handler(msg, process_order)


def process_order(message):
    user = message.from_user
    orders[user.id] = "❌ Не оплачен"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💬 Ответить", callback_data=f"reply_{user.id}"))

    bot.send_message(ADMIN_ID, f"""
📥 Заказ

👤 @{user.username}
🆔 {user.id}

📝 {message.text}

📊 Статус: ❌ Не оплачен
""", reply_markup=markup)

    bot.send_message(message.chat.id, "✅ Заказ отправлен")


# 📊 статус
@bot.message_handler(func=lambda m: m.text == "📊 Статус заказа")
def status(message):
    status = orders.get(message.from_user.id, "❌ Нет заказа")
    bot.send_message(message.chat.id, f"📊 Твой статус:\n{status}")


# 💳 оплата
@bot.message_handler(func=lambda m: m.text == "💳 Оплатить")
def pay(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("✅ Я оплатил")

    bot.send_message(message.chat.id, f"""
💳 VISA
{4196720050644946}
{NURBOLOT DUISHENBAI UULU}
""", reply_markup=markup)


# чек
@bot.message_handler(func=lambda m: m.text == "✅ Я оплатил")
def paid(message):
    waiting_payment[message.from_user.id] = True
    bot.send_message(message.chat.id, "Отправь чек")


@bot.message_handler(content_types=['photo'])
def check(message):
    if message.from_user.id not in waiting_payment:
        return

    user_id = message.from_user.id

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Принять", callback_data=f"ok_{user_id}"),
        types.InlineKeyboardButton("❌ Отклонить", callback_data=f"no_{user_id}")
    )

    bot.send_photo(ADMIN_ID, message.photo[-1].file_id, reply_markup=markup)

    bot.send_message(message.chat.id, "Чек отправлен")
    del waiting_payment[user_id]


# подтверждение
@bot.callback_query_handler(func=lambda c: c.data.startswith("ok_"))
def ok(call):
    user_id = int(call.data.split("_")[1])
    orders[user_id] = "🟡 Оплачен"

    bot.send_message(user_id, "✅ Оплата принята")
    bot.send_message(call.message.chat.id, "Ок")


# ❌ отказ
@bot.callback_query_handler(func=lambda c: c.data.startswith("no_"))
def no(call):
    user_id = int(call.data.split("_")[1])
    bot.send_message(user_id, "❌ Оплата не найдена")


# ⭐ отзыв
@bot.message_handler(func=lambda m: m.text == "⭐ Отзыв")
def review(message):
    reviews_wait[message.from_user.id] = True
    bot.send_message(message.chat.id, "Напиши отзыв:")


@bot.message_handler(func=lambda m: m.from_user.id in reviews_wait)
def save_review(message):
    user = message.from_user

    bot.send_message(ADMIN_ID, f"""
⭐ Новый отзыв

👤 @{user.username}
📝 {message.text}
""")

    bot.send_message(message.chat.id, "Спасибо за отзыв ❤️")
    del reviews_wait[user.id]


# 🖼 работы
@bot.message_handler(func=lambda m: m.text == "🖼 Наши работы")
def works(message):
    for file_id, text in WORKS:
        bot.send_photo(message.chat.id, file_id, caption=text)


# 💬 ответ
@bot.callback_query_handler(func=lambda c: c.data.startswith("reply_"))
def reply(call):
    user_id = int(call.data.split("_")[1])
    reply_dict[call.from_user.id] = user_id
bot.send_message(call.from_user.id, "Напиши ответ:")


@bot.message_handler(func=lambda m: m.from_user.id in reply_dict)
def send_reply(message):
    user_id = reply_dict[message.from_user.id]

    bot.send_message(user_id, f"💬 Админ:\n{message.text}")
    bot.send_message(message.chat.id, "Отправлено")

    del reply_dict[message.from_user.id]


bot.infinity_polling()
