import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

API_TOKEN = "8739134919:AAGsQBLIStXsdOktWwXc9BB1_pKhsUdxswQ"

# 👇 айди админов
ADMINS = [6498779131, 7299702298, 6034730945]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# 🔘 КНОПКИ
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton("🎨 Заказать дизайн"))
kb.add(KeyboardButton("💬 Помощь"))

# 🚀 СТАРТ
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "🔥 Добро пожаловать в FAHH DESIGNERS!\nВыбери действие:",
        reply_markup=kb
    )

# 🎨 ЗАКАЗ
@dp.message_handler(text="🎨 Заказать дизайн")
async def design(message: types.Message):
    await message.answer("✍️ Напиши, что тебе нужно (аватарка, превью и т.д.)")

# 💬 ПОМОЩЬ
@dp.message_handler(text="💬 Помощь")
async def help(message: types.Message):
    await message.answer("Я помогу тебе создать дизайн 🎨\nПросто напиши, что нужно!")

# 📩 ЛОВИМ ВСЕ СООБЩЕНИЯ
@dp.message_handler()
async def all_messages(message: types.Message):
    text = message.text

    # отправка админам
    for admin_id in ADMINS:
        await bot.send_message(
            admin_id,
            f"📩 Новая заявка!\n\n"
            f"👤 @{message.from_user.username}\n"
            f"🆔 {message.from_user.id}\n\n"
            f"💬 {text}"
        )

    await message.answer("✅ Заявка отправлена! Ожидай ответа 🙌")

# ▶️ ЗАПУСК
if name == 'main':
    executor.start_polling(dp, skip_updates=True)
