#!/bin/bash
# 0 8 * * 1 sh /home/user/market/backend/postgres_utils/delete_unpaid_orders.sh >> /home/user/market/backend/src/logs/delete_unpaid_order.log
PGPASSWORD=$POSTGRES_PASSWORD psql -d market -U cmarket -c "
DELETE FROM payments_orderproduct po where po.id in (
  SELECT
    o.id
  FROM payments_order o
  WHERE o.is_paid = false AND o.cash AND o.created_at < (SELECT CURRENT_TIMESTAMP - INTERVAL '7 day')
);
DELETE FROM payments_order o where o.id in (
  SELECT
    o.id
  FROM payments_order o
  WHERE o.is_paid = false AND o.cash AND o.created_at < (SELECT CURRENT_TIMESTAMP - INTERVAL '7 day')
);
"
