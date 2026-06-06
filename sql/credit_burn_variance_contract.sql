-- Board-readable Snowflake credit-burn variance contract.
-- Replace example schema names with Snowflake ACCOUNT_USAGE, QUERY_HISTORY, WAREHOUSE_METERING_HISTORY,
-- and tagging exports.
with warehouse_metering as (
  select
    warehouse_name,
    sum(credits_used) as monthly_credits
  from snowflake.account_usage.warehouse_metering_history
  where start_time >= dateadd(day, -30, current_timestamp())
  group by warehouse_name
),
query_health as (
  select
    warehouse_name,
    100.0 * count_if(error_code is not null) / nullif(count(*), 0) as failed_query_percent,
    100.0 * count_if(query_tag is null or query_tag = '') / nullif(count(*), 0) as unlabeled_query_percent
  from snowflake.account_usage.query_history
  where start_time >= dateadd(day, -30, current_timestamp())
  group by warehouse_name
)
select
  m.warehouse_name,
  m.monthly_credits,
  q.failed_query_percent,
  q.unlabeled_query_percent
from warehouse_metering m
left join query_health q using (warehouse_name);
