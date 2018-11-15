


CREATE TABLE IF NOT EXISTS wallet (
  uuid   uuid DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
  balance NUMERIC(12, 2) NOT NULL,
  currency currency_list,
  created_at TIMESTAMPTZ DEFAULT Now()
);

CREATE TABLE IF NOT EXISTS transfer (
  uuid   uuid DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
  amount NUMERIC(12, 2) NOT NULL,
  source_id uuid NOT NULL REFERENCES wallet(uuid),
  destination_id uuid NOT NULL REFERENCES wallet(uuid),
  created_at TIMESTAMPTZ DEFAULT Now()
);

CREATE TABLE IF NOT EXISTS transaction (
  uuid   uuid DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
  amount NUMERIC(12, 2) NOT NULL,
  wallet_id  uuid NOT NULL REFERENCES wallet(uuid),
  created_at TIMESTAMPTZ DEFAULT Now()
);
