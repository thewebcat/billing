CREATE EXTENSION pgcrypto;

--BEGIN TYPES
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'currency_list') THEN
    CREATE TYPE currency_list AS ENUM (
      'USD',
      'EUR',
      'CAD',
      'CNY');
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'transaction_type_list') THEN
    CREATE TYPE transaction_types_list AS ENUM (
      'deposit',
      'withdrawal',
      'transfer');
  END IF;
END$$;
--END create types

--BEGIN FUNCTIONS
CREATE OR REPLACE FUNCTION total_sum_function()
RETURNS trigger AS $$
BEGIN
  UPDATE "wallet" SET "balance" = "balance" + NEW."amount"
  WHERE "uuid" = NEW."wallet_id";
  RETURN NULL;
END;
$$ LANGUAGE plpgsql VOLATILE
   COST 100;

CREATE OR REPLACE FUNCTION make_transfer_function()
RETURNS trigger AS $$
BEGIN
  INSERT INTO "transaction" (amount, type, wallet_id) VALUES
  (-NEW."amount", 'transfer', NEW.source_id),
  (NEW."amount_converted", 'transfer', NEW.destination_id);
  RETURN NULL;
END;
$$ LANGUAGE plpgsql VOLATILE
   COST 100;
--END END FUNCTIONS