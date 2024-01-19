import uuid

import aiohttp

from config import Config


async def download_photo(
    file_id: str | int,
    config: Config,
    path: str = None,
) -> str:
    uri_info = f'https://api.telegram.org/bot{config.bot_token}/getFile?file_id={file_id}'
    uri = f'https://api.telegram.org/file/bot{config.bot_token}/'
    async with aiohttp.ClientSession() as request:
        async with request.get(uri_info) as response:
            img_path = (await response.json())['result']['file_path']
        async with request.get(uri + img_path) as img:
            filename = uuid.uuid4()
            path = path or '%s/%s.jpg' % (config.media_dir, filename)
            with open(path, 'wb') as f:
                f.write(await img.content.read())

    return f'images/{filename}.jpg'
