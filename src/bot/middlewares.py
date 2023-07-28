import asyncio

from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class AlbumMiddleware(BaseMiddleware):
    album_data: dict = {}

    def __init__(self, latency=0.01):
        self.latency = latency
        super().__init__()

    async def on_process_message(self, message, data):
        if not message.media_group_id:
            return None
        try:
            self.album_data[message.media_group_id].append(message)
            raise CancelHandler()
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            message.conf['is_last'] = True
            data['album'] = self.album_data[message.media_group_id]

    async def on_post_process_message(self, message, result, data):
        if message.media_group_id and message.conf.get('is_last'):
            del self.album_data[message.media_group_id]
