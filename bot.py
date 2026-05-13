import telebot

TOKEN = "8334869207:AAElRCsnU6jMldOyYSsVutKpWXvjAcd5paM"
MY_ID = 8776670480

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['text','photo','video','document','audio','voice','sticker'])
def forward_all(message):
    bot.copy_message(MY_ID, message.chat.id, message.message_id)

print("Bot started...")
bot.infinity_polling()
