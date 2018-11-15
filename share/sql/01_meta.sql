CREATE IF NOT EXISTS EXTENSION pgcrypto;

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
  IF
  INSERT INTO "transaction" (amount, wallet_id) VALUES
  (-NEW."amount", NEW.source_id),
  (NEW."amount", NEW.destination_id);
  RETURN NULL;
END;
$$ LANGUAGE plpgsql VOLATILE
   COST 100;
--END END FUNCTIONS

--BEGIN TRIGGERS
CREATE TRIGGER trigger_sum
  AFTER INSERT
  ON "transaction"
  FOR EACH ROW
  EXECUTE PROCEDURE total_sum_function();

CREATE TRIGGER trigger_sum
  AFTER INSERT
  ON "transfer"
  FOR EACH ROW
  EXECUTE PROCEDURE make_transfer_function();
--END END TRIGGERS