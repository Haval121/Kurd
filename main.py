import asyncio
import logging
from telegram import Update, ReactionTypeEmoji
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# توکەنی بۆتی یەکەم و دووەم
BOT_TOKEN_1 = "9169914698:AAE5meicD8QOHDZcVrFfrzLjzu70uVRjbTo"
BOT_TOKEN_2 = "9285144246:AAFtZ5i-b0UpH4tFz0R3IV3kyssWXurBDpU"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# فانکشنی بۆتی یەکەم (ڕیاکتی ❤️)
async def handle_video_bot1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if message and (message.video or (message.document and message.document.mime_type and "video" in message.document.mime_type)):
        try:
            await context.bot.set_message_reaction(
                chat_id=message.chat_id,
                message_id=message.id,
                reaction=[ReactionTypeEmoji("❤️")]
            )
        except Exception as e:
            print(f"Bot 1 Error: {e}")

# فانکشنی بۆتی دووەم (ڕیاکتی ❤️‍🔥)
async def handle_video_bot2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if message and (message.video or (message.document and message.document.mime_type and "video" in message.document.mime_type)):
        try:
            await context.bot.set_message_reaction(
                chat_id=message.chat_id,
                message_id=message.id,
                reaction=[ReactionTypeEmoji("❤️‍🔥")]
            )
        except Exception as e:
            print(f"Bot 2 Error: {e}")

async def run_bot_1():
    app1 = ApplicationBuilder().token(BOT_TOKEN_1).build()
    # چاودێری هەموو ڤیدیۆیەکی گروپەکان دەکات
    app1.add_handler(MessageHandler(filters.ChatType.GROUPS & (filters.VIDEO | filters.ATTACHMENT), handle_video_bot1))
    
    await app1.initialize()
    await app1.start()
    await app1.updater.start_polling()
    print("Bot 1 is running and ready for ❤️ reactions...")

async def run_bot_2():
    app2 = ApplicationBuilder().token(BOT_TOKEN_2).build()
    # چاودێری هەموو ڤیدیۆیەکی گروپەکان دەکات
    app2.add_handler(MessageHandler(filters.ChatType.GROUPS & (filters.VIDEO | filters.ATTACHMENT), handle_video_bot2))
    
    await app2.initialize()
    await app2.start()
    await app2.updater.start_polling()
    print("Bot 2 is running and ready for ❤️‍🔥 reactions...")

async def main():
    # کارپێکردنی هەردوو بۆتەکە پێکەوە لە یەک کاتدا
    await asyncio.gather(
        run_bot_1(),
        run_bot_2(),
        asyncio.Event().wait() # هێشتنەوەی بۆتەکان بە کراوەیی
    )

if __name__ == "__main__":
    asyncio.run(main())
    
