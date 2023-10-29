import os

import aiohttp


async def download_photo(file_id: int, path: str = None) -> str:
    uri_info = f'https://api.telegram.org/bot{os.getenv("BOT_TOKEN")}/getFile?file_id={file_id}'
    uri = f'https://api.telegram.org/file/bot{os.getenv("BOT_TOKEN")}/'
    async with aiohttp.ClientSession() as request:
        async with request.get(uri_info) as response:
            img_path = (await response.json())['result']['file_path']
        async with request.get(uri + img_path) as img:
            path = path or f'../../core/src/media/images/{file_id}.jpg'
            with open(path, 'wb') as f:
                f.write(await img.content.read())
    return f'images/{file_id}.jpg'
