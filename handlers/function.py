import os
import hashlib
import yt_dlp
import time
from aiogram.types import FSInputFile

def generate_url_id(url:str):
    return hashlib.md5(url.encode()).hexdigest()

async def download_and_send_media(bot, chat_id, url, media_type):
    ydl_opts = {
        'format': 'best[ext=mp4]' if media_type == "video" else 'bestaudio[ext=m4a]/best',
        'outtmpl': f'downloads/%(title)s.{"mp4" if media_type == "video" else "m4a"}',
    }
    try:
        start_time = time.time()

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url,download=True)
            filename = ydl.prepare_filename(info)

        end_time = time.time()
        elapsed_time = end_time - start_time

        media_file = FSInputFile(filename)
        if media_type == 'video':
            await bot.send_video(chat_id, media_file, caption=f"Here's your video! Loading time {elapsed_time:.2f} seconds.")
        else:
            await bot.send_audio(chat_id, media_file, caption=f"Here's your audio! Loading time {elapsed_time:.2f} seconds.")

        
        os.remove(filename)

    except Exception as e:
        await bot.send_message(chat_id, f'Error: {e}')
