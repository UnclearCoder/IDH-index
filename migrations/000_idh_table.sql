BEGIN;

CREATE TABLE IF NOT EXISTS idh (
  id int not null,
  date_time timestamptz not null,
  health_index float not null,
  health_index_adjusted float not null,
  income_index float not null,
  income_index_adjusted float not null,
  edu_index float not null,
  edu_index_adjusted float not null

);

CREATE TABLE IF NOT EXISTS idh_hyper (
  id int not null,
  date_time timestamptz not null,
  health_index float not null,
  health_index_adjusted float not null,
  income_index float not null,
  income_index_adjusted float not null,
  edu_index float not null,
  edu_index_adjusted float not null
);

SELECT create_hypertable('idh_hyper', 'date_time');

COMMIT;