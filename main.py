import telebot
from telebot import types

bot = telebot.TeleBot("8739134919:AAH8csG0v-Y3MTHO6U_UREeq7byPy3LuNnM")

ADMIN_ID = 6498779131
PREVIEW_ADMIN = 7299702298
VIDEO_ADMIN = 6034730945

reply_mode = {}
give_mode = {}

orders = {}
users = {}
history = {}
reviews = []

# ===== РАБОТЫ (ВСЕ) =====

PREVIEW_WORKS = [
"AgACAgIAAxkBAAICwmm8RUJeGjWegRvmdyKF9Q6B8MruAAJ2EWsbH6rgSRbRjfLboF-EAQADAgADeQADOgQ",
"AgACAgIAAxkBAAICwWm8RUI8aqXrLjoODXZ4LDlvIhHVAAJ1EWsbH6rgSQL8ts1pj65-AQADAgADeQADOgQ",
"AgACAgIAAxkBAAICw2m8RUJk_QABh2kNOYfJBm6lSXboTwACdxFrGx-q4EkKZxE8q-t0TwEAAwIAA3kAAzoE",
"AgACAgIAAxkBAAICxGm8RUKTM86HtHX5Rhyq_62Bs1DoAAJ5EWsbH6rgSTNd0uY5QfOyAQADAgADeQADOgQ",
"AgACAgIAAxkBAAICxWm8RUIYPT_otVwQJHmka35cXngfAAJ6EWsbH6rgSU_DX65UgJ8VAQADAgADeQADOgQ"
]

VIDEO_WORKS = [
"BAACAgIAAxkBAAIC0mm8Rekw5ukwWBFVAyco8zW3j72ZAAKWlQACaK_hSXIxxtYbLvLpOgQ",
"BAACAgIAAxkBAAIC0Wm8RekpxUww7uiHYY7L8Ag__mdxAAKVlQACaK_hSfXjbhFTV4RrOgQ"
]

CARD_WORKS = [
"AgACAgIAAxkBAAIC1mm8Rip2nbtbWZlhvSwnOHRTgWKSAALHEWsbiQzoSR8BlDvXLE5GAQADAgADeQADOgQ",
"AgACAgIAAxkBAAIC1Wm8RiolwMBtr0gjBKs_qmXLcQToAAJMEmsbX7bQSTr_kz7qzyS6AQADAgADeQADOgQ"
]

# ===== СТАРТ =====

@bot.message_handler(commands=['start'])
def start(m):
    users[m.from_user.id] = m.from_user.username

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("📂 Работы")
    kb.add("🎨 Заказать дизайн", "🤖 Бот / Сайт / Игра")
    kb.add("🎬 Видео/Монтаж")
    kb.add("🎥 Превью", "💳 Карточка")
    kb.add("📊 Статус", "🧾 История")
    kb.add("⭐ Отзывы")

    if m.from_user.id == ADMIN_ID:
        kb.add("📦 Отдать заказ", "📋 Заказы")

    bot.send_message(m.chat.id, "FAAAHHH DESIGNERS 👑", reply_markup=kb)

# ===== РАБОТЫ =====

@bot.message_handler(func=lambda m: m.text == "📂 Работы")
def works(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🎥 Превью работы", "🎬 Видео работы")
    kb.add("💳 Карточки", "🔙 Назад")
    bot.send_message(m.chat.id, "Выбери раздел:", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "🎥 Превью работы")
def preview_works(m):
    for p in PREVIEW_WORKS:
        bot.send_photo(m.chat.id, p)

@bot.message_handler(func=lambda m: m.text == "🎬 Видео работы")
def video_works(m):
    for v in VIDEO_WORKS:
        bot.send_video(m.chat.id, v)

@bot.message_handler(func=lambda m: m.text == "💳 Карточки")
def card_works(m):
    for c in CARD_WORKS:
        bot.send_photo(m.chat.id, c)

@bot.message_handler(func=lambda m: m.text == "🔙 Назад")
def back(m):
    start(m)

# ===== ЗАКАЗ =====

def send_order(m, admin, cat):
    u = m.from_user
    users[u.id] = u.username

    orders[u.id] = "⏳ Ожидается"
    history.setdefault(u.id, []).append(f"{cat}: {m.text}")

    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("✅ Принять", callback_data=f"acc_{u.id}"),
        types.InlineKeyboardButton("❌ Отказать", callback_data=f"dec_{u.id}")
    )
    kb.add(types.InlineKeyboardButton("💬 Ответ", callback_data=f"rep_{u.id}"))

    bot.send_message(admin, f"""
📥 Новый заказ ({cat})

👤 @{u.username}
🆔 {u.id}

📝 {m.text}
""", reply_markup=kb)

    bot.send_message(m.chat.id, "✅ Заказ отправлен!")

def ask(m, admin, cat):
    msg = bot.send_message(m.chat.id, "Опиши заказ и спросите цену!")
    bot.register_next_step_handler(msg, lambda x: send_order(x, admin, cat))

# ===== КНОПКИ ЗАКАЗОВ =====

@bot.message_handler(func=lambda m: m.text == "🎨 Заказать дизайн")
def design(m): ask(m, ADMIN_ID, "Дизайн")

@bot.message_handler(func=lambda m: m.text == "🤖 Бот / Сайт / Игра")
def prog(m): ask(m, ADMIN_ID, "Бот/Сайт/Игра")

@bot.message_handler(func=lambda m: m.text == "🎬 Видео/Монтаж")
def video(m): ask(m, VIDEO_ADMIN, "Видео")

@bot.message_handler(func=lambda m: m.text == "🎥 Превью")
def preview(m): ask(m, PREVIEW_ADMIN, "Превью")

@bot.message_handler(func=lambda m: m.text == "💳 Карточка")
def card(m): ask(m, ADMIN_ID, "Карточка")

# ===== СТАТУС =====

@bot.message_handler(func=lambda m: m.text == "📊 Статус")
def status(m):
    bot.send_message(m.chat.id, orders.get(m.from_user.id, "❌ Нет заказа"))

# ===== ИСТОРИЯ =====

@bot.message_handler(func=lambda m: m.text == "🧾 История")
def hist(m):
    h = history.get(m.from_user.id)
    bot.send_message(m.chat.id, "\n".join(h) if h else "Пусто")

# ===== ОТЗЫВЫ =====

@bot.message_handler(func=lambda m: m.text == "⭐ Отзывы")
def review_menu(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("✍️ Оставить отзыв", "📖 Смотреть отзывы", "🔙 Назад")
    bot.send_message(m.chat.id, "Отзывы:", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "✍️ Оставить отзыв")
def add_review(m):
    msg = bot.send_message(m.chat.id, "Напиши отзыв:")
    bot.register_next_step_handler(msg, save_review)

def save_review(m):
    reviews.append(f"@{m.from_user.username}: {m.text}")
    bot.send_message(m.chat.id, "✅ Сохранено")

@bot.message_handler(func=lambda m: m.text == "📖 Смотреть отзывы")
def show_reviews(m):
    bot.send_message(m.chat.id, "\n\n".join(reviews) if reviews else "Нет отзывов")

# ===== АДМИН СПИСОК =====

@bot.message_handler(func=lambda m: m.text == "📋 Заказы")
def admin_orders(m):
    if m.from_user.id != ADMIN_ID:
        return

    if not orders:
        bot.send_message(m.chat.id, "❌ Нет заказов")
        return

    text = ""
    for uid, status in orders.items():
        name = users.get(uid) or uid
        text += f"👤 {name} | {uid}\n📊 {status}\n\n"

    bot.send_message(m.chat.id, text)

# ===== CALLBACK =====

@bot.callback_query_handler(func=lambda c: c.data.startswith("acc_"))
def acc(c):
    uid = int(c.data.split("_")[1])
    orders[uid] = "✅ Принято"
    bot.send_message(uid, "✅ Принято")

@bot.callback_query_handler(func=lambda c: c.data.startswith("dec_"))
def dec(c):
    uid = int(c.data.split("_")[1])
    orders[uid] = "❌ Отменено"
    bot.send_message(uid, "❌ Отменено")

@bot.callback_query_handler(func=lambda c: c.data.startswith("rep_"))
def rep(c):
    uid = int(c.data.split("_")[1])
    reply_mode[c.from_user.id] = uid
    bot.send_message(c.from_user.id, "Напиши ответ")

# ===== ОТДАТЬ =====

@bot.message_handler(func=lambda m: m.text == "📦 Отдать заказ")
def give(m):
    if m.from_user.id != ADMIN_ID:
        return

    kb = types.InlineKeyboardMarkup()
    for uid, name in users.items():
        kb.add(types.InlineKeyboardButton(f"@{name}" if name else str(uid), callback_data=f"give_{uid}"))

    bot.send_message(m.chat.id, "Выбери пользователя:", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("give_"))
def give_user(c):
    uid = int(c.data.split("_")[1])
    give_mode[c.from_user.id] = uid
    bot.send_message(c.from_user.id, "Отправь готовый заказ")

# ===== ОБЩИЙ ОБРАБОТЧИК =====

@bot.message_handler(content_types=['text','photo','video'])
def all(m):

    if m.from_user.id in reply_mode:
        uid = reply_mode[m.from_user.id]

        if m.text:
            bot.send_message(uid, f"💬 Админ:\n{m.text}")
        elif m.photo:
            bot.send_photo(uid, m.photo[-1].file_id)
        elif m.video:
            bot.send_video(uid, m.video.file_id)

        del reply_mode[m.from_user.id]
        return

    if m.from_user.id in give_mode:
        uid = give_mode[m.from_user.id]

        if m.photo:
            bot.send_photo(uid, m.photo[-1].file_id, caption="✅ Заказ готов")
        elif m.video:
            bot.send_video(uid, m.video.file_id, caption="✅ Заказ готов")
        elif m.text:
            bot.send_message(uid, "✅ Заказ готов\n" + m.text)

        orders[uid] = "✅ Готов"
        del give_mode[m.from_user.id]
        return

# ===== ЗАПУСК =====

bot.infinity_polling()
