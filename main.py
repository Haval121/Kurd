import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters

# توکەنی بۆتەکەت
BOT_TOKEN = "8370918902:AAG2tXhRwDlBP4UhTgB80CBWww7HUgccqmk"

# ڕێکخستنی لاگین (Logging) بۆ بینینی هەڵەکان
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def save_video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    user = update.effective_user
    
    # پشکنین بۆ ئەوەی بزانین پەیامەکە ڕایپڵەی کراوە یان نا
    if not message.reply_to_message:
        await message.reply_text("تکایە ئەم فەرمانە بە **ڕایپڵەی** کردن لەسەر ڤیدیۆ بنووسە.")
        return

    target_msg = message.reply_to_message
    
    # پشکنین بۆ دڵنیابوونەوە لەوەی ئایا ڤیدیۆیە یان دۆکیومێنتێکی ڤیدیۆییە
    if target_msg.video:
        file_id = target_msg.video.file_id
        caption = target_msg.caption or "فەرموو ئەمەش ڤیدیۆکەت 👇"
    elif target_msg.document and target_msg.document.mime_type and "video" in target_msg.document.mime_type:
        file_id = target_msg.document.file_id
        caption = target_msg.caption or "فەرموو ئەمەش ڤیدیۆکەت 👇"
    else:
        await message.reply_text("❌ ئەم پەیامەی ڕایپڵەت کردووە ڤیدیۆ نییە!")
        return

    user_id = user.id
    user_mention = user.mention_html()

    try:
        # ناردنی ڤیدیۆکە بۆ چاتی تایبەتی بە file_id
        await context.bot.send_video(
            chat_id=user_id,
            video=file_id,
            caption=caption
        )
        
        # وەڵامدانەوە لە گروپدا بە مێنشن کردنی بەکارهێنەرەکە
        await message.reply_text(
            f"✅ {user_mention}، ڤیدیۆکەت بۆ نێردرا بۆ چاتی تایبەتی (Private)!",
            parse_mode="HTML"
        )
    
    except Exception as e:
        # ئەگەر کەسەکە چاتی بۆتەکە نەکردبێتەوە
        await message.reply_text("⚠️ ناتوانم ڤیدیۆکەت بۆ بنێرم. تکایە سەرەتا سەردانی چاتی تایبەتی بۆت بکە و (Start)ـی بکە.")

def main():
    # دروستکردنی ئەپلیکەیشنی بۆت
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # زیادکردنی فەرمانەکە بۆ گروپەکان تەنها
    group_filter = filters.ChatType.GROUPS & filters.command("save")
    application.add_handler(CommandHandler("save", save_video_handler, filters=group_filter))

    print("Bot is up and running...")
    # دەستپێکردنی بۆت
    application.run_polling()

if __name__ == "__main__":
    main()
    
