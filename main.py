import telebot
from telebot import types

API_TOKEN = "8739134919:AAH8csG0v-Y3MTHO6U_UREeq7byPy3LuNnM"
bot = telebot.TeleBot(API_TOKEN)

# 👑 главный админ
ADMIN_ID = 6498779131

# 👨‍🎨 исполнители
PREVIEW_ADMIN = 7299702298
VIDEO_ADMIN = 6034730945

reply_dict = {}
orders = {}
reviews_wait = {}

# 🖼 ПРЕВЬЮ
PREVIEW_WORKS = [
    ("AgACAgIAAxkBAAICwmm8RUJeGjWegRvmdyKF9Q6B8MruAAJ2EWsbH6rgSRbRjfLboF-EAQADAgADeQADOgQ", "🔥 Превью"),
    ("AgACAgIAAxkBAAICwWm8RUI8aqXrLjoODXZ4LDlvIhHVAAJ1EWsbH6rgSQL8ts1pj65-AQADAgADeQADOgQ", "🔥 Превью"),
    ("AgACAgIAAxkBAAICw2m8RUJk_QABh2kNOYfJBm6lSXboTwACdxFrGx-q4EkKZxE8q-t0TwEAAwIAA3kAAzoE", "🔥 Превью"),
    ("AgACAgIAAxkBAAICxGm8RUKTM86HtHX5Rhyq_62Bs1DoAAJ5EWsbH6rgSTNd0uY5QfOyAQADAgADeQADOgQ", "🔥 Превью"),
    ("AgACAgIAAxkBAAICxWm8RUIYPT_otVwQJHmka35cXngfAAJ6EWsbH6rgSU_DX65UgJ8VAQADAgADeQADOgQ", "🔥 Превью"),
    ("AgACAgIAAxkBAAICxmm8RUIldkrNUUG1sLw95yFKHxZGAAJ7EWsbH6rgSdkYjLLlck96AQADAgADeQADOgQ", "🔥 Превью"),
]

# 🎥 ВИДЕО
VIDEO_WORKS = [
    ("BAACAgIAAxkBAAIC0mm8Rekw5ukwWBFVAyco8zW3j72ZAAKWlQACaK_hSXIxxtYbLvLpOgQ", "🎬 Монтаж"),
    ("BAACAgIAAxkBAAIC0Wm8RekpxUww7uiHYY7L8Ag__mdxAAKVlQACaK_hSfXjbhFTV4RrOgQ", "🎬 ИИ Видео"),
]

# 💳 КАРТОЧКИ
CARD_WORKS = [
    ("AgACAgIAAxkBAAIC1mm8Rip2nbtbWZlhvSwnOHRTgWKSAALHEWsbiQzoSR8BlDvXLE5GAQADAgADeQADOgQ", "💳 Карточка"),
    ("AgACAgIAAxkBAAIC1Wm8RiolwMBtr0gjBKs_qmXLcQToAAJMEmsbX7bQSTr_kz7qzyS6AQADAgADeQADOgQ", "💳 Карточка"),
]


# 🚀 СТАРТ
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("🎨 Заказать дизайн")
    markup.add("🤖 Бот / Сайт / Игра", "🎬 ИИ Видео / Монтаж")
    markup.add("🎥 Превью YouTube")
    markup.add("💳 Заказать карточку")  # 👈 добавили
    markup.add("🖼 Работы превью", "🎥 Работы видео")
    markup.add("💳 Работы карточки")
    markup.add("📊 Статус заказа", "⭐ Отзыв")

    bot.send_message(message.chat.id, "FAAAHHH DESIGNERS 👑", reply_markup=markup)


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


# 🎨
@bot.message_handler(func=lambda m: m.text == "🎨 Заказать дизайн")
def design(message):
    msg = bot.send_message(message.chat.id, "Опиши заказ и спросите цену!")
    bot.register_next_step_handler(msg, lambda m: send_order(m, ADMIN_ID, "Дизайн"))


# 🤖
@bot.message_handler(func=lambda m: m.text == "🤖 Бот / Сайт / Игра")
def bot_site(message):
    msg = bot.send_message(message.chat.id, "Опиши заказ и спросите цену!")
    bot.register_next_step_handler(msg, lambda m: send_order(m, ADMIN_ID, "Бот/Сайт/Игра"))


# 🎬
@bot.message_handler(func=lambda m: m.text == "🎬 ИИ Видео / Монтаж")
def video(message):
    msg = bot.send_message(message.chat.id, "Опиши заказ и спросите цену!")
    bot.register_next_step_handler(msg, lambda m: send_order(m, VIDEO_ADMIN, "Монтаж"))


# 🎥
@bot.message_handler(func=lambda m: m.text == "🎥 Превью YouTube")
def preview(message):
    msg = bot.send_message(message.chat.id, "Опиши заказ и спросите цену!")
    bot.register_next_step_handler(msg, lambda m: send_order(m, PREVIEW_ADMIN, "Превью"))


# 💳 КАРТОЧКА
@bot.message_handler(func=lambda m: m.text == "💳 Заказать карточку")
def card(message):
    msg = bot.send_message(message.chat.id, "Опиши заказ и спросите цену!")
    bot.register_next_step_handler(msg, lambda m: send_order(m, ADMIN_ID, "Карточка"))


# 🖼 ПРЕВЬЮ РАБОТЫ
@bot.message_handler(func=lambda m: m.text == "🖼 Работы превью")
def preview_works(message):
    for file_id, text in PREVIEW_WORKS:
        bot.send_photo(message.chat.id, file_id, caption=text)


# 🎥 ВИДЕО РАБОТЫ
@bot.message_handler(func=lambda m: m.text == "🎥 Работы видео")
def video_works(message):
    for file_id, text in VIDEO_WORKS:
        bot.send_video(message.chat.id, file_id, caption=text)


# 💳 КАРТОЧКИ РАБОТЫ
@bot.message_handler(func=lambda m: m.text == "💳 Работы карточки")
def card_works(message):
    for file_id, text in CARD_WORKS:
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


# 💬 ОТВЕТ АДМИНА
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
