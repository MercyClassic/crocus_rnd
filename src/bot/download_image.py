import io
import os

import aiohttp
from django.core.files.images import ImageFile


async def download_photo(file_id):
    uri_info = f'https://api.telegram.org/bot{os.getenv("BOT_TOKEN")}/getFile?file_id='
    uri = f'https://api.telegram.org/file/bot{os.getenv("BOT_TOKEN")}/'
    async with aiohttp.ClientSession() as request:
        async with request.get(uri_info + file_id) as response:
            img_path = (await response.json())['result']['file_path']
        async with request.get(uri + img_path) as img:
            return ImageFile(io.BytesIO(await img.content.read()), name=f'{file_id}.jpg')
