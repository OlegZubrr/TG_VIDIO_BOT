from aiogram import Bot,Router,F
from aiogram.types import CallbackQuery

from handlers.function import download_and_send_media
import url_storage as storage

router = Router()

@router.callback_query(lambda callback: 'video' in callback.data or 'audio' in callback.data)
async def format_selection(callback: CallbackQuery, bot: Bot):
    storage.url_storage = storage.load_url_storage()
    action,url_id = callback.data.split('|')
    url = storage.url_storage.get(url_id)
    if not url :
        await callback.answer('Error! The URL won\'t be found!')
        return
    await callback.answer('Confirmed!')
    if action == 'video':
        await callback.message.answer("I'm starting to upload a video...")
        await download_and_send_media(bot, callback.message.chat.id, url, media_type='video')
    elif action == 'audio':
        await callback.message.answer("I'm starting to upload an audio...")
        await download_and_send_media(bot, callback.message.chat.id, url, media_type='audio')
