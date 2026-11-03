import os
from pyrogram import Client, filters
from pyrogram.types import Message

# زانیارییە تایبەتەکانت کە دابووت
API_ID = 36234377
API_HASH = "5e199e2ae89cc1c42a6a4853951ff98f"
BOT_TOKEN = "8370918902:AAG2tXhRwDlBP4UhTgB80CBWww7HUgccqmk"

# دروستکردنی کۆمستەنسی بۆتەکە
app = Client(
    "video_save_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("save") & filters.group)
async def save_video_handler(client: Client, message: Message):
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

    user_id = message.from_user.id

    try:
        # ناردنی ڤیدیۆکە بۆ چاتی تایبەتی بە file_id
        await client.send_video(
            chat_id=user_id,
            video=file_id,
            caption=caption
        )
        
        # وەڵامدانەوە لە گروپدا بە مێنشن کردنی بەکارهێنەرەکە
        await message.reply_text(f"✅ {message.from_user.mention}، ڤیدیۆکەت بۆ نێردرا بۆ چاتی تایبەتی (Private)!")
    
    except Exception as e:
        # ئەگەر کەسەکە چاتی بۆتەکە نەکردبێتەوە
        await message.reply_text("⚠️ ناتوانم ڤیدیۆکەت بۆ بنێرم. تکایە سەرەتا سەردانی چاتی تایبەتی بۆت بکە و (Start)ـی بکە.")

# دەستپێکردنی بۆت
print("Bot is up and running...")
app.run()
