import telebot
from openai import OpenAI

# زانیارییەکانی بۆت و API
BOT_TOKEN = "8670204681:AAGm7q4lckaaWGSxI_A2XsphtzaDvLBYqj8"
API_BASE_URL = "https://api.notrack.ai/v1"
API_KEY = "sk-notrack-93d1aea5cb8360688f1840f62dcaf2fe5e02117a476406ec"
MODEL_NAME = "notrack-uncensored"

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

# هەڵگرتنی مێژووی گفتوگۆ بۆ هەر بەکارهێنەرێک (user_id -> list of messages)
user_histories = {}
MAX_HISTORY = 20  # ژمارەی زۆرترین نامەی پێشوو کە بۆتەکە لە بیری دەمێنێت


def get_history(user_id: int) -> list:
    if user_id not in user_histories:
        user_histories[user_id] = [
            {"role": "system", "content": "You are a helpful AI assistant."}
        ]
    return user_histories[user_id]


@bot.message_handler(commands=["start"])
def handle_start(message):
    user_id = message.from_user.id
    user_histories[user_id] = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]
    bot.reply_to(
        message,
        "سڵاو! بەخێربێیت بۆ بۆتی چات.\n"
        "هەر پرسیار یان بابەتێکت هەیە بینووسە تا وەڵامت بدەمەوە.\n"
        "بۆ سڕینەوەی مێژووی چات، فەرمانی /clear بنێرە.",
    )


@bot.message_handler(commands=["clear"])
def handle_clear(message):
    user_id = message.from_user.id
    user_histories[user_id] = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]
    bot.reply_to(message, "✅ مێژووی گفتوگۆکەت سڕایەوە.")


@bot.message_handler(func=lambda msg: True, content_types=["text"])
def handle_chat(message):
    user_id = message.from_user.id
    user_text = message.text.strip()

    if not user_text:
        return

    # پیشاندانی دۆخی "typing..." لە تیلگرام
    bot.send_chat_action(message.chat.id, "typing")

    history = get_history(user_id)
    history.append({"role": "user", "content": user_text})

    # سنووردارکردنی درێژیی مێژوو بۆ ئەوەی تووشی کێشەی token limit نەبێت
    if len(history) > MAX_HISTORY + 1:
        user_histories[user_id] = [history[0]] + history[-MAX_HISTORY:]
        history = user_histories[user_id]

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=history,
        )
        reply_text = response.choices[0].message.content or "وەڵامێک نەگەڕایەوە."
        history.append({"role": "assistant", "content": reply_text})

        # ئەگەر وەڵامەکە زۆر درێژ بوو (زیاتر لە ٤٠٩٦ پیت)، بە چەند بەش دەینێرێت
        for i in range(0, len(reply_text), 4096):
            bot.reply_to(message, reply_text[i : i + 4096])

    except Exception as e:
        # لابردنی دوایین نامەی بەکارهێنەر ئەگەر هەڵەیەک ڕوویدا
        history.pop()
        bot.reply_to(message, f"⚠️ کێشەیەک لە پەیوەندیکردن بە API ڕوویدا:\n{e}")


if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling(skip_pending=True)
