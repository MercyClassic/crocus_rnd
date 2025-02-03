#!/bin/sh
DATE=`date +"%Y-%m-%d"`
database=market
PGPASSWORD=$POSTGRES_PASSWORD pg_dump -d $database -U cmarket | gzip > /tmp-market/$DATE-$database.dump.gz
cd /home/user/market/backend/core/src/media
tar -czf /tmp-market/$DATE-market-images.tar.gz images
/usr/bin/find /tmp-market  -type f -mtime +30 -exec rm -rf {} \;
