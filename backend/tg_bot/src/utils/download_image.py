import os
import uuid

import aiohttp
from dependency_injector.wiring import Provide, inject

from config import Config
from container import Container


@inject
async def download_photo(
    file_id: int,
    path: str = None,
    config: Config = Provide[Container.config],
) -> str:
    uri_info = f'https://api.telegram.org/bot{os.getenv("BOT_TOKEN")}/getFile?file_id={file_id}'
    uri = f'https://api.telegram.org/file/bot{os.getenv("BOT_TOKEN")}/'
    async with aiohttp.ClientSession() as request:
        async with request.get(uri_info) as response:
            img_path = (await response.json())['result']['file_path']
        async with request.get(uri + img_path) as img:
            filename = uuid.uuid4()
            path = path or '%s/%s.jpg' % (config.MEDIA_DIR, filename)
            with open(path, 'wb') as f:
                f.write(await img.content.read())
    return f'images/{filename}.jpg'
