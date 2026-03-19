import telebot

API_TOKEN = "8739134919:AAH8csG0v-Y3MTHO6U_UREeq7byPy3LuNnM"
bot = telebot.TeleBot(API_TOKEN)


# 📸 ФОТО
@bot.message_handler(content_types=['photo'])
def get_photo_id(message):
    file_id = message.photo[-1].file_id
    bot.send_message(message.chat.id, f"📸 PHOTO ID:\n{file_id}")


# 🎥 ВИДЕО
@bot.message_handler(content_types=['video'])
def get_video_id(message):
    file_id = message.video.file_id
    bot.send_message(message.chat.id, f"🎥 VIDEO ID:\n{file_id}")


# 📄 ДОКУМЕНТЫ (если вдруг кидаешь как файл)
@bot.message_handler(content_types=['document'])
def get_doc_id(message):
    file_id = message.document.file_id
    bot.send_message(message.chat.id, f"📄 FILE ID:\n{file_id}")


# 🚀 ЗАПУСК
bot.infinity_polling()
