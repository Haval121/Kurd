import requests
from pyrogram import Client, filters
import re
import os

# زانیارییەکانی تۆ
BOT_TOKEN = "9236530543:AAEvLFhnYdV_gxI-iqmd50UusPIeAus_eZc"
APP_ID = 36234377
API_HASH = "5e199e2ae89cc1c42a6a4853951ff98f"

app = Client("my_bot", api_id=APP_ID, api_hash=API_HASH)

def download_video_from_freeporn(url):
    """
    دابەزاندنی ڤیدیۆ لە سایتی FreePornVideos
    """
    try:
        # سەرەتا لاپەڕەکە دەخوێنینەوە
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None
        
        html_content = response.text
        
        # لێرەدا دەگەڕێین بۆ لینکی ڤیدیۆکە
        # لەم سایتەدا، لینکی ڤیدیۆکە لەناو تاقگی <video> یان <source>ـدایە
        # بەڵام زۆرجار لینکەکان بە شێوەی JSON یان data-src هەڵدەسەنگێن
        
        # هەوڵدان بۆ دۆزینەوەی لینکی mp4
        video_url_match = re.search(r'src="([^"]+\.mp4[^"]*)"', html_content)
        
        if not video_url_match:
            # هەوڵدان بۆ دۆزینەوەی لینکی تر (بە تایبەتی بۆ ئەم سایتە)
            video_url_match = re.search(r'"file":\s*"([^"]+)"', html_content)
            
        if video_url_match:
            video_url = video_url_match.group(1)
            # دابەزاندنی فایلەکە
            video_response = requests.get(video_url, stream=True, headers=headers)
            filename = f"video_{os.urandom(8).hex()}.mp4"
            
            with open(filename, 'wb') as f:
                for chunk in video_response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            return filename
        else:
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("سڵاو! تکایە لینکی ڤیدیۆکە لە سایتی FreePornVideos بنێرە.")

@app.on_message(filters.regex(r'https?://[^\s]+'))
async def handle_link(client, message):
    url = message.text
    if "freepornvideos" in url or "freepornvideos.xxx" in url:
        await message.reply_text("چاوەڕوان بە...")
        video_file = download_video_from_freeporn(url)
        
        if video_file:
            await message.reply_video(video_file)
            os.remove(video_file)  # پاککردنەوەی فایلەکە دوای ناردن
        else:
            await message.reply_text("نەتوانرا ڤیدیۆکە بدۆزرێتەوە.")
    else:
        await message.reply_text("تکایە لینکێک لە سایتی FreePornVideos بنێرە.")

if __name__ == "__main__":
    app.run()
