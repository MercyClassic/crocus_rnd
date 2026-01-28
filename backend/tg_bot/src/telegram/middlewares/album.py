import asyncio
from collections.abc import Callable

from aiogram import BaseMiddleware, types


class AlbumMiddleware(BaseMiddleware):
    def __init__(self, latency: float = 0.01):
        self.latency = latency
        super().__init__()
        self.album_data = {}

    async def __call__(
        self,
        handler: Callable,
        event: types.TelegramObject,
        data: dict,
    ) -> None:
        message: types.Message = event.message
        if not message or (not message.media_group_id and not message.photo):
            await handler(event, data)
        else:
            try:
                self.album_data[message.media_group_id].append(message)
            except KeyError:
                self.album_data[message.media_group_id] = [message]
                await asyncio.sleep(self.latency)

                data['_is_last'] = True
                data['album'] = self.album_data[message.media_group_id]
                await handler(event, data)

            if data.get('_is_last'):
                del self.album_data[message.media_group_id]
                del data['_is_last']
