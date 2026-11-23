import time
import requests
import telebot

BOT_TOKEN = "8670204681:AAHSY36xruqYzPksQyyH7BgRMk3W1jCnEgo"
API_URL = "https://api.notrack.ai/v1/chat/completions"
API_KEY = "sk-notrack-93d1aea5cb8360688f1840f62dcaf2fe5e02117a476406ec"
MODEL_NAME = "notrack-uncensored"

bot = telebot.TeleBot(BOT_TOKEN)
user_histories = {}
MAX_HISTORY = 20


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

    bot.send_chat_action(message.chat.id, "typing")

    history = get_history(user_id)
    history.append({"role": "user", "content": user_text})

    if len(history) > MAX_HISTORY + 1:
        user_histories[user_id] = [history[0]] + history[-MAX_HISTORY:]
        history = user_histories[user_id]

    try:
        res = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL_NAME,
                "messages": history,
            },
            timeout=60,
        )
        res.raise_for_status()
        data = res.json()
        reply_text = data["choices"][0]["message"]["content"] or "وەڵامێک نەگەڕایەوە."
        history.append({"role": "assistant", "content": reply_text})

        for i in range(0, len(reply_text), 4096):
            bot.reply_to(message, reply_text[i : i + 4096])

    except Exception as e:
        history.pop()
        bot.reply_to(message, f"⚠️ کێشەیەک لە پەیوەندیکردن بە API ڕوویدا:\n{e}")


if __name__ == "__main__":
    print("Bot is running...")
    while True:
        try:
            bot.infinity_polling(
                skip_pending=False,
                timeout=25,
                long_polling_timeout=25,
            )
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(20)
            
