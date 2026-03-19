import telebot
from telebot import types

API_TOKEN = "8739134919:AAH8csG0v-Y3MTHO6U_UREeq7byPy3LuNnM"
bot = telebot.TeleBot(API_TOKEN)

ADMIN_ID = 6498779131
PREVIEW_ADMIN = 7299702298
VIDEO_ADMIN = 6034730945

reply_dict = {}
orders = {}
users = {}
order_history = {}

# 🖼 ПРЕВЬЮ
PREVIEW_WORKS = [
    "AgACAgIAAxkBAAICwmm8RUJeGjWegRvmdyKF9Q6B8MruAAJ2EWsbH6rgSRbRjfLboF-EAQADAgADeQADOgQ",
    "AgACAgIAAxkBAAICwWm8RUI8aqXrLjoODXZ4LDlvIhHVAAJ1EWsbH6rgSQL8ts1pj65-AQADAgADeQADOgQ"
]

# 🎥 ВИДЕО
VIDEO_WORKS = [
    "BAACAgIAAxkBAAIC0mm8Rekw5ukwWBFVAyco8zW3j72ZAAKWlQACaK_hSXIxxtYbLvLpOgQ",
    "BAACAgIAAxkBAAIC0Wm8RekpxUww7uiHYY7L8Ag__mdxAAKVlQACaK_hSfXjbhFTV4RrOgQ"
]

# 💳 КАРТОЧКИ
CARD_WORKS = [
    "AgACAgIAAxkBAAIC1mm8Rip2nbtbWZlhvSwnOHRTgWKSAALHEWsbiQzoSR8BlDvXLE5GAQADAgADeQADOgQ",
    "AgACAgIAAxkBAAIC1Wm8RiolwMBtr0gjBKs_qmXLcQToAAJMEmsbX7bQSTr_kz7qzyS6AQADAgADeQADOgQ"
]


# 🚀 СТАРТ
@bot.message_handler(commands=['start'])
def start(message):
    users[message.from_user.id] = message.from_user.username

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎨 Заказать дизайн")
    markup.add("🤖 Бот / Сайт / Игра", "🎬 ИИ Видео / Монтаж")
    markup.add("🎥 Превью YouTube")
    markup.add("💳 Заказать карточку")
    markup.add("🖼 Работы превью", "🎥 Работы видео")
    markup.add("💳 Работы карточки")
    markup.add("📊 Статус заказа", "🧾 История заказов")

    if message.from_user.id == ADMIN_ID:
        markup.add("📦 Отдать заказ", "📋 Список заказов")

    bot.send_message(message.chat.id, "FAAAHHH DESIGNERS 👑", reply_markup=markup)


# 📤 ЗАКАЗ
def send_order(message, target_id, category):
    user = message.from_user
    username = f"@{user.username}" if user.username else "Без ника"

    users[user.id] = user.username
    orders[user.id] = "⏳ Ожидайте"

    if user.id not in order_history:
        order_history[user.id] = []

    order_history[user.id].append(f"{category}: {message.text}")

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Принять", callback_data=f"accept_{user.id}"),
        types.InlineKeyboardButton("❌ Отказать", callback_data=f"decline_{user.id}")
    )
    markup.add(types.InlineKeyboardButton("💬 Ответить", callback_data=f"reply_{user.id}"))

    bot.send_message(target_id, f"""
📥 Новый заказ ({category})

👤 {username}
🆔 {user.id}

📝 {message.text}

📊 Статус: ⏳ Ожидайте
""", reply_markup=markup)

    bot.send_message(message.chat.id, "✅ Заказ отправлен!")


# КНОПКИ ЗАКАЗА
def ask(message, text, admin, category):
    msg = bot.send_message(message.chat.id, "Опиши заказ и спросите цену!")
    bot.register_next_step_handler(msg, lambda m: send_order(m, admin, category))


@bot.message_handler(func=lambda m: m.text == "🎨 Заказать дизайн")
def design(m): ask(m, "", ADMIN_ID, "Дизайн")

@bot.message_handler(func=lambda m: m.text == "💳 Заказать карточку")
def card(m): ask(m, "", ADMIN_ID, "Карточка")

@bot.message_handler(func=lambda m: m.text == "🎬 ИИ Видео / Монтаж")
def video(m): ask(m, "", VIDEO_ADMIN, "Видео")

@bot.message_handler(func=lambda m: m.text == "🎥 Превью YouTube")
def preview(m): ask(m, "", PREVIEW_ADMIN, "Превью")


# 🖼 РАБОТЫ
@bot.message_handler(func=lambda m: m.text == "🖼 Работы превью")
def show_preview(m):
    for p in PREVIEW_WORKS:
        bot.send_photo(m.chat.id, p)

@bot.message_handler(func=lambda m: m.text == "🎥 Работы видео")
def show_video(m):
    for v in VIDEO_WORKS:
        bot.send_video(m.chat.id, v)

@bot.message_handler(func=lambda m: m.text == "💳 Работы карточки")
def show_card(m):
    for c in CARD_WORKS:
        bot.send_photo(m.chat.id, c)


# 📊 СТАТУС
@bot.message_handler(func=lambda m: m.text == "📊 Статус заказа")
def status(m):
    bot.send_message(m.chat.id, orders.get(m.from_user.id, "❌ Нет заказа"))


# 🧾 ИСТОРИЯ
@bot.message_handler(func=lambda m: m.text == "🧾 История заказов")
def history(m):
    hist = order_history.get(m.from_user.id)
    if not hist:
        bot.send_message(m.chat.id, "❌ История пустая")
        return

    text = "🧾 Твои заказы:\n\n"
    for i, h in enumerate(hist, 1):
        text += f"{i}. {h}\n"

    bot.send_message(m.chat.id, text)


# 📋 АДМИН СПИСОК
@bot.message_handler(func=lambda m: m.text == "📋 Список заказов")
def admin_orders(m):
    if m.from_user.id != ADMIN_ID:
        return

    if not orders:
        bot.send_message(m.chat.id, "❌ Нет заказов")
        return

    text = "📋 Заказы:\n\n"
    for uid, st in orders.items():
        text += f"{users.get(uid)} | {uid}\n{st}\n\n"

    bot.send_message(m.chat.id, text)


# ✅ / ❌
@bot.callback_query_handler(func=lambda c: c.data.startswith("accept_"))
def accept(c):
    uid = int(c.data.split("_")[1])
    orders[uid] = "✅ Принято, ожидайте"
    bot.send_message(uid, "✅ Принято")

@bot.callback_query_handler(func=lambda c: c.data.startswith("decline_"))
def decline(c):
    uid = int(c.data.split("_")[1])
    orders[uid] = "❌ Отменено"
    bot.send_message(uid, "❌ Отменено")


# 💬 ОТВЕТ
@bot.callback_query_handler(func=lambda c: c.data.startswith("reply_"))
def reply(c):
    uid = int(c.data.split("_")[1])
    reply_dict[c.from_user.id] = uid
    bot.send_message(c.from_user.id, "Отправь сообщение/фото/видео")


@bot.message_handler(content_types=['text', 'photo', 'video'])
def reply_send(m):
    if m.from_user.id in reply_dict:
        uid = reply_dict[m.from_user.id]

        if m.text:
            bot.send_message(uid, f"💬 Админ:\n{m.text}")
        elif m.photo:
            bot.send_photo(uid, m.photo[-1].file_id)
        elif m.video:
            bot.send_video(uid, m.video.file_id)

        del reply_dict[m.from_user.id]


# 📦 ОТДАТЬ ЗАКАЗ
@bot.message_handler(func=lambda m: m.text == "📦 Отдать заказ")
def give(m):
    if m.from_user.id != ADMIN_ID:
        return

    markup = types.InlineKeyboardMarkup()
    for uid in users:
        name = users[uid] if users[uid] else uid
        markup.add(types.InlineKeyboardButton(str(name), callback_data=f"give_{uid}"))

    bot.send_message(m.chat.id, "Выбери пользователя:", reply_markup=markup)


@bot.callback_query_handler(func=lambda c: c.data.startswith("give_"))
def choose(c):
    uid = int(c.data.split("_")[1])
    reply_dict[c.from_user.id] = uid
    bot.send_message(c.from_user.id, "Отправь фото/видео заказа")


@bot.message_handler(content_types=['photo', 'video'])
def send_done(m):
    if m.from_user.id in reply_dict:
        uid = reply_dict[m.from_user.id]

        if m.photo:
            bot.send_photo(uid, m.photo[-1].file_id, caption="✅ Заказ готов")
        elif m.video:
            bot.send_video(uid, m.video.file_id, caption="✅ Заказ готов")

        orders[uid] = "✅ Готов"
        del reply_dict[m.from_user.id]


bot.infinity_polling()
