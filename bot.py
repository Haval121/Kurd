import telebot
import os

TOKEN = "8334869207:AAElRCsnU6jMldOyYSsVutKpWXvjAcd5paM"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
bot.reply_to(message, "سڵاو، بۆتەکە کار دەکات ✅")

bot.infinity_polling()
