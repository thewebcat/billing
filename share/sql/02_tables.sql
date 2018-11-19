CREATE TABLE IF NOT EXISTS client (
  uuid   uuid DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
  first_name  VARCHAR(255) NOT NULL,
  last_name   VARCHAR(255),
  country     VARCHAR(255) NOT NULL,
  city        VARCHAR(255) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT Now()
);

CREATE TABLE IF NOT EXISTS wallet (
  uuid   uuid DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
  balance NUMERIC(12, 2) DEFAULT 0 NOT NULL,
  client_id uuid NOT NULL REFERENCES client(uuid),
  currency currency_list,
  created_at TIMESTAMPTZ DEFAULT Now()
);

CREATE TABLE IF NOT EXISTS transfer (
  uuid   uuid DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
  amount NUMERIC(12, 2) DEFAULT 0 NOT NULL,
  amount_converted NUMERIC(12, 2) DEFAULT 0 NOT NULL,
  source_id uuid NOT NULL REFERENCES wallet(uuid),
  destination_id uuid NOT NULL REFERENCES wallet(uuid),
  created_at TIMESTAMPTZ DEFAULT Now()
);

CREATE TABLE IF NOT EXISTS transaction (
  uuid   uuid DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
  type   transaction_types_list,
  amount NUMERIC(12, 2) DEFAULT 0 NOT NULL,
  wallet_id  uuid NOT NULL REFERENCES wallet(uuid),
  created_at TIMESTAMPTZ DEFAULT Now()
);

CREATE TABLE rate (
  date DATE NOT NULL PRIMARY KEY,
  currency JSONB
);
CREATE INDEX ON rate USING gin (currency);

--BEGIN TRIGGERS
CREATE TRIGGER trigger_sum
  AFTER INSERT
  ON "transaction"
  FOR EACH ROW
  EXECUTE PROCEDURE total_sum_function();

CREATE TRIGGER trigger_transfer
  AFTER INSERT
  ON "transfer"
  FOR EACH ROW
  EXECUTE PROCEDURE make_transfer_function();
--END END TRIGGERS
