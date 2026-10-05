INSERT INTO inv_products (id, isin, name, product_type, currency, risk_level, annual_cost_pct, income_type, data_source)
VALUES
(1, NULL, 'Liquidez / monetario EUR', 'monetario', 'EUR', 1, 0.1000, 'acumulacion', 'manual'),
(2, NULL, 'Renta fija EUR corto plazo', 'renta_fija', 'EUR', 2, 0.2000, 'acumulacion', 'manual'),
(3, NULL, 'Cartera mixta conservadora', 'mixto', 'EUR', 3, 0.5000, 'acumulacion', 'manual'),
(4, NULL, 'Renta variable global', 'renta_variable', 'EUR', 5, 0.2500, 'acumulacion', 'manual')
ON DUPLICATE KEY UPDATE name = VALUES(name);

INSERT INTO inv_portfolios (id, name, description, initial_amount, monthly_income_target)
VALUES
(1, 'Muy conservadora', 'Cartera demo con mayor peso en liquidez y renta fija.', 300000, 650),
(2, 'Conservadora equilibrada', 'Cartera demo equilibrada entre renta fija y crecimiento moderado.', 300000, 650),
(3, 'Conservadora crecimiento', 'Cartera demo conservadora con mayor peso de crecimiento global.', 300000, 650)
ON DUPLICATE KEY UPDATE name = VALUES(name);

INSERT INTO inv_portfolio_targets (portfolio_id, product_id, target_pct)
VALUES
(1, 1, 30.0000), (1, 2, 45.0000), (1, 3, 20.0000), (1, 4, 5.0000),
(2, 1, 20.0000), (2, 2, 35.0000), (2, 3, 35.0000), (2, 4, 10.0000),
(3, 1, 15.0000), (3, 2, 30.0000), (3, 3, 35.0000), (3, 4, 20.0000);

INSERT INTO inv_prices (product_id, price_date, price, currency, source, source_type)
VALUES
(1, CURRENT_DATE, 100.00000000, 'EUR', 'demo', 'manual'),
(2, CURRENT_DATE, 100.00000000, 'EUR', 'demo', 'manual'),
(3, CURRENT_DATE, 100.00000000, 'EUR', 'demo', 'manual'),
(4, CURRENT_DATE, 100.00000000, 'EUR', 'demo', 'manual')
ON DUPLICATE KEY UPDATE price = VALUES(price);
