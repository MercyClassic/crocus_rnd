import logging
import os
import smtplib
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logging.basicConfig(
    level='INFO',
    filename='src/logs/smtp.log',
    format='{asctime} - {levelname} - {message}',
    style='{',
)
logger = logging.getLogger(__name__)


def send_backup_db_email():
    sender = os.environ['EMAIL_HOST']
    email_password = os.environ['EMAIL_HOST_PASSWORD']
    to_notification = os.environ['TO_NOTIFICATION']
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, email_password)
    msg = MIMEMultipart()
    msg['Subject'] = 'Backup database postgres'
    msg['To'] = to_notification
    msg['From'] = sender
    current_time = datetime.now()
    msg.attach(
        MIMEText(
            'Бэкап базы данных crocus rnd'
            f' на момент времени {current_time.strftime("%d.%m.%Y %H:%M")}',
        ),
    )
    message_file = MIMEBase('application', 'octet-stream')
    with open(f'/tmp-market/{datetime.now().date()}-market.dump.gz', 'rb') as fp:
        message_file.set_payload(fp.read())
        encoders.encode_base64(message_file)
    message_file.add_header(
        'Content-Disposition',
        'attachment; filename=%s' % f'{current_time.date()}-market.dump.gz',
    )
    msg.attach(message_file)
    server.sendmail(sender, to_notification, msg.as_string())


if __name__ == '__main__':
    try:
        send_backup_db_email()
    except Exception as ex:
        logger.error(ex)
