-- =========================================================
-- UC189 - PostgreSQL Database Schema
-- AI Voice-Based Insurance Quoting Assistant
-- =========================================================

CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    age INTEGER NOT NULL,
    gender VARCHAR(32),
    occupation VARCHAR(128),
    annual_income DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    location VARCHAR(128),
    smoking_status BOOLEAN DEFAULT FALSE,
    pre_existing_conditions JSONB DEFAULT '[]'::jsonb,
    family_members INTEGER DEFAULT 1,
    insurance_type VARCHAR(64) DEFAULT 'health',
    risk_score DOUBLE PRECISION DEFAULT 0.2,
    risk_category VARCHAR(32) DEFAULT 'low',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
);

CREATE TABLE IF NOT EXISTS policies (
    policy_id VARCHAR(64) PRIMARY KEY,
    policy_name VARCHAR(128) NOT NULL,
    provider VARCHAR(128) NOT NULL,
    tier VARCHAR(64) DEFAULT 'standard',
    insurance_type VARCHAR(64) DEFAULT 'health',
    base_premium DOUBLE PRECISION NOT NULL,
    coverage_amount DOUBLE PRECISION NOT NULL,
    deductible DOUBLE PRECISION DEFAULT 500.0,
    key_benefits JSONB DEFAULT '[]'::jsonb,
    limitations JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
);

CREATE TABLE IF NOT EXISTS quotes (
    quote_id VARCHAR(64) PRIMARY KEY,
    customer_id VARCHAR(64) REFERENCES customers(customer_id) ON DELETE SET NULL,
    policy_id VARCHAR(64) REFERENCES policies(policy_id) ON DELETE SET NULL,
    policy_name VARCHAR(128) NOT NULL,
    insurance_type VARCHAR(64) NOT NULL,
    monthly_premium DOUBLE PRECISION NOT NULL,
    annual_premium DOUBLE PRECISION NOT NULL,
    coverage_amount DOUBLE PRECISION NOT NULL,
    deductible DOUBLE PRECISION NOT NULL DEFAULT 500.0,
    term_years INTEGER DEFAULT 1,
    coverage_details JSONB DEFAULT '[]'::jsonb,
    add_ons JSONB DEFAULT '[]'::jsonb,
    status VARCHAR(32) DEFAULT 'active',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
);

CREATE TABLE IF NOT EXISTS voice_interactions (
    interaction_id VARCHAR(64) PRIMARY KEY,
    session_id VARCHAR(128) NOT NULL,
    customer_id VARCHAR(64) REFERENCES customers(customer_id) ON DELETE SET NULL,
    user_message TEXT NOT NULL,
    assistant_message TEXT NOT NULL,
    intent VARCHAR(64) DEFAULT 'general_inquiry',
    sentiment VARCHAR(32) DEFAULT 'neutral',
    sentiment_score DOUBLE PRECISION DEFAULT 0.5,
    duration_seconds DOUBLE PRECISION DEFAULT 0.0,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
);

CREATE INDEX IF NOT EXISTS idx_customers_risk ON customers(risk_category);
CREATE INDEX IF NOT EXISTS idx_quotes_customer ON quotes(customer_id);
CREATE INDEX IF NOT EXISTS idx_interactions_session ON voice_interactions(session_id);
