import telebot
from telebot import types

bot = telebot.TeleBot("8739134919:AAH8csG0v-Y3MTHO6U_UREeq7byPy3LuNnM")

ADMIN_ID = 6498779131
PREVIEW_ADMIN = 7299702298
VIDEO_ADMIN = 6034730945

users = {}
orders = {}
history = {}
reviews = []

user_state = {}
reply_mode = {}
give_mode = {}

# ===== РАБОТЫ =====
PREVIEW_WORKS = [
"AgACAgIAAxkBAAICwmm8RUJeGjWegRvmdyKF9Q6B8MruAAJ2EWsbH6rgSRbRjfLboF-EAQADAgADeQADOgQ"
]

VIDEO_WORKS = [
"BAACAgIAAxkBAAIC0mm8Rekw5ukwWBFVAyco8zW3j72ZAAKWlQACaK_hSXIxxtYbLvLpOgQ"
]

CARD_WORKS = [
"AgACAgIAAxkBAAIC1mm8Rip2nbtbWZlhvSwnOHRTgWKSAALHEWsbiQzoSR8BlDvXLE5GAQADAgADeQADOgQ"
]

# ===== ГЛАВНОЕ МЕНЮ =====
def main_menu(user_id):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add("🛒 Заказать", "📂 Работы")
    kb.add("📊 Статус", "🧾 История")
    kb.add("⭐ Отзывы")

    if user_id == ADMIN_ID:
        kb.add("📦 Отдать заказ", "📋 Заказы")

    return kb

# ===== СТАРТ =====
@bot.message_handler(commands=['start'])
def start(m):
    users[m.from_user.id] = m.from_user.username
    bot.send_message(
        m.chat.id,
        "👑 FAAA HHH DESIGNERS\n\nВыбери действие:",
        reply_markup=main_menu(m.from_user.id)
    )

# ===== АВТО ОТВЕТ =====
def auto_reply(user_id):
    bot.send_message(
        user_id,
        "🤖 Заявка отправлена!\nАдмин скоро ответит.\n\n⏳ Ожидайте..."
    )

# ===== МЕНЮ ЗАКАЗА =====
@bot.message_handler(func=lambda m: m.text == "🛒 Заказать")
def order_menu(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🤖 Бот / Сайт / Игра")
    kb.add("🎬 Видео / ИИ", "🎥 Превью")
    kb.add("💳 Карточка")
    kb.add("🔙 Назад")

    bot.send_message(m.chat.id, "Выбери услугу:", reply_markup=kb)

# ===== ВЫБОР УСЛУГ =====
def ask_order(m, admin_id, category):
    user_state[m.from_user.id] = (admin_id, category)
    bot.send_message(m.chat.id, "✍️ Опиши заказ\n\n(спросите цену!)")

@bot.message_handler(func=lambda m: m.text == "🤖 Бот / Сайт / Игра")
def prog(m): ask_order(m, ADMIN_ID, "Программирование")

@bot.message_handler(func=lambda m: m.text == "🎬 Видео / ИИ")
def video(m): ask_order(m, VIDEO_ADMIN, "Видео")

@bot.message_handler(func=lambda m: m.text == "🎥 Превью")
def preview(m): ask_order(m, PREVIEW_ADMIN, "Превью")

@bot.message_handler(func=lambda m: m.text == "💳 Карточка")
def card(m): ask_order(m, ADMIN_ID, "Карточка")

# ===== РАБОТЫ =====
@bot.message_handler(func=lambda m: m.text == "📂 Работы")
def works(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🎥 Превью работы", "🎬 Видео работы")
    kb.add("💳 Карточки", "🔙 Назад")
    bot.send_message(m.chat.id, "Работы:", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "🎥 Превью работы")
def show_prev(m):
    for p in PREVIEW_WORKS:
        bot.send_photo(m.chat.id, p)

@bot.message_handler(func=lambda m: m.text == "🎬 Видео работы")
def show_vid(m):
    for v in VIDEO_WORKS:
        bot.send_video(m.chat.id, v)

@bot.message_handler(func=lambda m: m.text == "💳 Карточки")
def show_card(m):
    for c in CARD_WORKS:
        bot.send_photo(m.chat.id, c)

# ===== ПРИЕМ ЗАКАЗА =====
@bot.message_handler(content_types=['text','photo','video'])
def handler(m):

    uid = m.from_user.id
    users[uid] = m.from_user.username

    # ===== СОЗДАНИЕ ЗАКАЗА =====
    if uid in user_state:
        admin_id, cat = user_state[uid]

        text = m.text if m.text else "Медиа заказ"

        orders[uid] = "⏳ Ожидается"
        history.setdefault(uid, []).append(cat)

        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton("✅", callback_data=f"acc_{uid}"),
            types.InlineKeyboardButton("❌", callback_data=f"dec_{uid}")
        )
        kb.add(types.InlineKeyboardButton("💬 Ответ", callback_data=f"rep_{uid}"))

        bot.send_message(admin_id, f"📥 {cat}\n@{m.from_user.username}\n{text}", reply_markup=kb)

        auto_reply(uid)
        del user_state[uid]
        return

    # ===== ОТВЕТ АДМИНА =====
    if uid in reply_mode:
        user = reply_mode[uid]

        if m.text:
            bot.send_message(user, m.text)
        elif m.photo:
            bot.send_photo(user, m.photo[-1].file_id)
        elif m.video:
            bot.send_video(user, m.video.file_id)

        del reply_mode[uid]
        return

    # ===== ОТДАТЬ ЗАКАЗ =====
    if uid in give_mode:
        user = give_mode[uid]

        if m.text:
            bot.send_message(user, "✅ Заказ готов\n" + m.text)
        elif m.photo:
            bot.send_photo(user, m.photo[-1].file_id, caption="✅ Заказ готов")
        elif m.video:
            bot.send_video(user, m.video.file_id, caption="✅ Заказ готов")

        orders[user] = "✅ Готов"
        del give_mode[uid]
        return

# ===== CALLBACK =====
@bot.callback_query_handler(func=lambda c: True)
def callbacks(c):

    uid = int(c.data.split("_")[1])

    if c.data.startswith("acc"):
        orders[uid] = "✅ Принято"
        bot.send_message(uid, "✅ Принято")

    elif c.data.startswith("dec"):
        orders[uid] = "❌ Отменено"
        bot.send_message(uid, "❌ Отменено")

    elif c.data.startswith("rep"):
        reply_mode[c.from_user.id] = uid
        bot.send_message(c.from_user.id, "✍️ Ответь")

    elif c.data.startswith("give"):
        give_mode[c.from_user.id] = uid
        bot.send_message(c.from_user.id, "📦 Отправь заказ")

# ===== ОТДАТЬ =====
@bot.message_handler(func=lambda m: m.text == "📦 Отдать заказ")
def give(m):
    if m.from_user.id != ADMIN_ID:
        return

    kb = types.InlineKeyboardMarkup()
    for uid, name in users.items():
        kb.add(types.InlineKeyboardButton(
            f"@{name}" if name else str(uid),
            callback_data=f"give_{uid}"
        ))

    bot.send_message(m.chat.id, "Выбери пользователя:", reply_markup=kb)

# ===== СПИСОК ЗАКАЗОВ =====
@bot.message_handler(func=lambda m: m.text == "📋 Заказы")
def orders_list(m):
    if m.from_user.id != ADMIN_ID:
        return

    text = ""
    for u, st in orders.items():
        text += f"{users.get(u)} — {st}\n"

    bot.send_message(m.chat.id, text or "Нет заказов")

# ===== СТАТУС =====
@bot.message_handler(func=lambda m: m.text == "📊 Статус")
def status(m):
    bot.send_message(m.chat.id, orders.get(m.from_user.id, "Нет заказа"))

# ===== ИСТОРИЯ =====
@bot.message_handler(func=lambda m: m.text == "🧾 История")
def hist(m):
    bot.send_message(m.chat.id, "\n".join(history.get(m.from_user.id, [])) or "Пусто")

# ===== ОТЗЫВЫ =====
@bot.message_handler(func=lambda m: m.text == "⭐ Отзывы")
def rev(m):
    bot.send_message(m.chat.id, "\n\n".join(reviews) or "Нет отзывов")

# ===== ЗАПУСК =====
bot.infinity_polling()
