import glob
import json
import logging
import os
import requests
from datetime import datetime

logging.basicConfig(
    level='INFO',
    filename='src/logs/backup.log',
    format='{asctime} - {levelname} - {message}',
    style='{',
)
logger = logging.getLogger(__name__)

TELEGRAM_API_URL = 'https://api.telegram.org/bot{token}/{method}'
LAST_MESSAGE_IDS_FILE = '/tmp-market/.last_backup_message_ids.json'


def load_last_message_ids() -> list[int]:
    try:
        with open(LAST_MESSAGE_IDS_FILE, 'r') as f:
            data = json.load(f)
            return data if isinstance(data, list) and len(data) > 0 else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_message_ids(message_ids: list[int]) -> None:
    with open(LAST_MESSAGE_IDS_FILE, 'w') as f:
        json.dump(message_ids, f)


def delete_messages(bot_token: str, chat_id: str, message_ids: list[int]) -> None:
    for message_id in message_ids:
        response = requests.post(
            url=TELEGRAM_API_URL.format(token=bot_token, method='deleteMessage'),
            data={'chat_id': chat_id, 'message_id': message_id},
        )
        if not response.ok:
            logger.warning(f'Не удалось удалить сообщение {message_id}: {response.text}')


def send_document(bot_token: str, chat_id: str, file_path: str, caption: str = '') -> int:
    filename = os.path.basename(file_path)
    with open(file_path, 'rb') as fp:
        response = requests.post(
            url=TELEGRAM_API_URL.format(token=bot_token, method='sendDocument'),
            data={'chat_id': chat_id, 'caption': caption},
            files={'document': (filename, fp, 'application/octet-stream')},
        )
    response.raise_for_status()
    return response.json()['result']['message_id']


def send_backup_db_with_images() -> None:
    bot_token: str = os.environ['BOT_TOKEN']
    chat_id: str = os.environ['BACKUP_TELEGRAM_CHAT_ID']
    current_time: datetime = datetime.now()
    date_str: str = current_time.strftime('%d.%m.%Y %H:%M')
    date_prefix: str = str(current_time.date())

    sent_message_ids: list[int] = []

    db_backup_path: str = f'/tmp-market/{date_prefix}-market.dump.gz'
    message_id: int = send_document(
        bot_token=bot_token,
        chat_id=chat_id,
        file_path=db_backup_path,
        caption=f'Бэкап базы данных crocus rnd на момент времени {date_str}',
    )
    sent_message_ids.append(message_id)

    image_parts: list[str] = sorted(glob.glob(f'/tmp-market/{date_prefix}-market-images.tar.gz.part_*'))
    total_parts: int = len(image_parts)

    for index, part_path in enumerate(image_parts, start=1):
        message_id = send_document(
            bot_token=bot_token,
            chat_id=chat_id,
            file_path=part_path,
            caption=f'Изображения — часть {index} из {total_parts}',
        )
        sent_message_ids.append(message_id)

    last_message_ids: list[int] = load_last_message_ids()
    if last_message_ids:
        delete_messages(bot_token, chat_id, last_message_ids)

    save_message_ids(sent_message_ids)
    logger.info(f'Бэкап успешно отправлен: {len(sent_message_ids)} сообщений.')


if __name__ == '__main__':
    try:
        send_backup_db_with_images()
    except Exception as ex:
        logger.error(ex)
