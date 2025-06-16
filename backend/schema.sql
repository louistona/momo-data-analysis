CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    sender TEXT,
    receiver TEXT,
    amount FLOAT,
    date TIMESTAMP,
    transaction_type TEXT
);

CREATE INDEX IF NOT EXISTS idx_transaction_message_date ON transactions (message, date);