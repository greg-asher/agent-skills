create table usage_events (
  event_id text primary key,
  account_id text not null,
  units integer not null,
  recorded_at timestamp not null
);

create table job_checkpoints (
  job_name text primary key,
  completed_through date not null,
  updated_at timestamp not null
);
