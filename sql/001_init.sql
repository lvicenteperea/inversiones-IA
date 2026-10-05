CREATE TABLE IF NOT EXISTS inv_products (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    isin VARCHAR(20) NULL,
    name VARCHAR(255) NOT NULL,
    product_type VARCHAR(50) NOT NULL,
    currency CHAR(3) NOT NULL DEFAULT 'EUR',
    risk_level TINYINT NULL,
    annual_cost_pct DECIMAL(8,4) NULL,
    income_type VARCHAR(30) NULL,
    data_source VARCHAR(100) NULL,
    active TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX ix_inv_products_isin (isin)
);

CREATE TABLE IF NOT EXISTS inv_portfolios (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NULL,
    initial_amount DECIMAL(18,4) NOT NULL,
    monthly_income_target DECIMAL(18,4) NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS inv_portfolio_targets (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    portfolio_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    target_pct DECIMAL(8,4) NOT NULL,
    CONSTRAINT fk_inv_targets_portfolio FOREIGN KEY (portfolio_id) REFERENCES inv_portfolios(id),
    CONSTRAINT fk_inv_targets_product FOREIGN KEY (product_id) REFERENCES inv_products(id)
);

CREATE TABLE IF NOT EXISTS inv_transactions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    portfolio_id BIGINT NOT NULL,
    product_id BIGINT NULL,
    transaction_date DATE NOT NULL,
    transaction_type VARCHAR(30) NOT NULL,
    amount DECIMAL(18,4) NOT NULL,
    units DECIMAL(24,8) NULL,
    price DECIMAL(18,8) NULL,
    notes TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_inv_transactions_portfolio FOREIGN KEY (portfolio_id) REFERENCES inv_portfolios(id),
    CONSTRAINT fk_inv_transactions_product FOREIGN KEY (product_id) REFERENCES inv_products(id)
);

CREATE TABLE IF NOT EXISTS inv_prices (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    product_id BIGINT NOT NULL,
    price_date DATE NOT NULL,
    price DECIMAL(18,8) NOT NULL,
    currency CHAR(3) NOT NULL DEFAULT 'EUR',
    source VARCHAR(100) NOT NULL,
    source_type VARCHAR(30) NOT NULL DEFAULT 'manual',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_product_date (product_id, price_date),
    CONSTRAINT fk_inv_prices_product FOREIGN KEY (product_id) REFERENCES inv_products(id)
);
