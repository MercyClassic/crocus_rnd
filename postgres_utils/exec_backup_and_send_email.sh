#!/bin/sh
# 0 8 * * 1 sh /home/user/market/postgres_utils/exec_backup_and_send_email.sh >> /var/log/market/send_backup_email.log
chdir /home/user/market/postgres_utils/
sh create_backup.sh
python3 send_email.py
