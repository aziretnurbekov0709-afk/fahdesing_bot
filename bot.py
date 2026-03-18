import telebot

TOKEN = "8739134919:AAGsQBLIStXsdOktWwXc9BB1_pKhsUdxswQ"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот 🤖")

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.chat.id, message.text)

bot.polling()
