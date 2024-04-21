from aiogram import Bot


async def download_image(
        bot: Bot,
        file_id: str,
        media_dir: str,
) -> str:
    file = await bot.get_file(file_id)
    path = f'{media_dir}/{file_id}.jpg'
    await bot.download_file(file.file_path, path)
    return file_id
