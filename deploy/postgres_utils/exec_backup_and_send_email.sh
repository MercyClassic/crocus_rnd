#!/bin/sh
# 0 8 * * 1 sh /home/user/market/deploy/postgres_utils/exec_backup_and_send_email.sh >> /home/user/market/backend/core/src/logs/smtp.log
cd /home/user/market/deploy/postgres_utils/
sh create_backup.sh
cd /home/user/market/backend/core
poetry run python3.11 /home/user/market/deploy/postgres_utils/send_email.py
