#!/bin/sh
# 0 8 * * 1 sh /home/user/market/deploy/postgres_utils/exec_backup_and_send_email.sh >> /home/user/market/backend/src/logs/send_backup_email.log
chdir /home/user/market/deploy/postgres_utils/
sh create_backup.sh
python3 send_email.py
