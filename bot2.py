import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json

TOKEN = "8795882175:AAHv4ZO7gFK9cS5thDOHl36lt5N94i7quBU"
ADMIN_ID = 5313754716
CHANNEL = "@pamay_cts"

bot = telebot.TeleBot(TOKEN)

try:
    with open("videos.json","r") as f:
        videos=json.load(f)
except:
    videos={}

def save():
    with open("videos.json","w") as f:
        json.dump(videos,f)

def menu():
    kb=InlineKeyboardMarkup()
    for k in videos:
        kb.add(InlineKeyboardButton(k,callback_data=k))
    return kb

@bot.message_handler(commands=['start'])
def start(m):
    txt="""╭━━━━━━━━━━━━━━━━━━━
ئەزیزم جۆینی چەناڵەکەمان بکە 😘
┃
┃ ⚡️ t.me/pamay_cts
┃
╰━━━━━━━━━━━━━━━━

بۆ بینی ڤیدۆ بەشک هەڵبژێرە👇"""
    bot.send_message(m.chat.id,txt,reply_markup=menu())

@bot.callback_query_handler(func=lambda c:True)
def call(c):
    if c.data in videos:
        bot.send_video(c.message.chat.id,videos[c.data])

@bot.message_handler(commands=['add'])
def add(m):
    if m.from_user.id==ADMIN_ID:
        msg=bot.reply_to(m,"ناوی بەش بنێرە")
        bot.register_next_step_handler(msg,get_name)

def get_name(m):
    name=m.text
    msg=bot.reply_to(m,"ڤیدیۆ بنێرە")
    bot.register_next_step_handler(msg,save_video,name)

def save_video(m,name):
    if m.video:
        videos[name]=m.video.file_id
        save()
        bot.reply_to(m,"زیادکرا ✅")

@bot.message_handler(commands=['del'])
def delete(m):
    if m.from_user.id==ADMIN_ID:
        name=m.text.replace('/del ','')
        if name in videos:
            del videos[name]
            save()
            bot.reply_to(m,"سڕایەوە ✅")

print("Bot started")
bot.infinity_polling()
