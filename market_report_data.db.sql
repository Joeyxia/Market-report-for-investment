-- Create market_data table
CREATE TABLE market_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL,
    metric_text TEXT,
    source TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert data for 2026-02-28
-- Monetary Policy & Liquidity
INSERT INTO market_data (date, category, metric_name, metric_value, metric_text, source) VALUES 
('2026-02-27', 'Monetary Policy', '10Y-3M Spread (bps)', 118, '+118 bps', 'U.S. Treasury'),
('2026-02-27', 'Monetary Policy', 'SOFR', 3.65, '3.65%', 'Federal Reserve'),
('2026-02-27', 'Monetary Policy', 'Fed Balance Sheet', 6600, '$6.60T', 'Federal Reserve');

-- Real Economy & Leading Indicators
INSERT INTO market_data (date, category, metric_name, metric_value, metric_text, source) VALUES 
('2025-12-31', 'Real Economy', 'GDP Growth Rate', 1.4, '1.4%', 'BEA'),
('2026-02-27', 'Real Economy', 'Core CPI', 2.5, '2.5%', 'BLS');

-- Corporate Fundamentals & Valuation
INSERT INTO market_data (date, category, metric_name, metric_value, metric_text, source) VALUES 
('2026-02-27', 'Corporate', 'Forward P/E', 20.3, '20.3x', 'Market Data'),
('2026-02-27', 'Corporate', 'ERP Big 7', 0.9, '0.9%', 'Market Data'),
('2026-02-27', 'Corporate', 'ERP S&P 493', 2.2, '2.2%', 'Market Data');

-- Labor Market & Consumer Health
INSERT INTO market_data (date, category, metric_name, metric_value, metric_text, source) VALUES 
('2026-02-27', 'Labor Market', 'Unemployment Rate', 4.3, '4.3%', 'BLS'),
('2026-02-27', 'Labor Market', 'Credit Card Delinquency Rate', 3.2, '3.2%', 'Federal Reserve');

-- Housing Market
INSERT INTO market_data (date, category, metric_name, metric_value, metric_text, source) VALUES 
('2026-02-27', 'Housing', 'Mortgage Rate', 6.0, '6.00%', 'Freddie Mac'),
('2026-02-27', 'Housing', 'Existing Home Sales', 392, '392K', 'NAR');

-- Market Sentiment & Cross-Asset Volatility
INSERT INTO market_data (date, category, metric_name, metric_value, metric_text, source) VALUES 
('2026-02-27', 'Volatility', 'VIX Index', 18.7, '18.7', 'CBOE'),
('2026-02-27', 'Volatility', 'MOVE Index', 67.8, '67.8', 'Bloomberg');

-- Cryptocurrency Market Indicators
INSERT INTO market_data (date, category, metric_name, metric_value, metric_text, source) VALUES 
('2026-02-28', 'Crypto', 'Bitcoin Price', 67500, '$67,500', 'CoinMarketCap'),
('2026-02-28', 'Crypto', 'USDC Market Cap', 75.5, '$75.5B', 'CoinMarketCap');

-- AI Development Indicators
INSERT INTO market_data (date, category, metric_name, metric_value, metric_text, source) VALUES 
('2026-02-27', 'AI', 'OpenRouter Monthly Tokens', 30000, '30T tokens', 'OpenRouter'),
('2026-02-27', 'AI', 'NVIDIA Delivery Lead Time', 26, '26 weeks', 'Market Data'),
('2026-02-27', 'AI', 'Cloud AI Revenue Growth', 43, '43% YoY', 'Market Data');

-- Commodities & External Macro
INSERT INTO market_data (date, category, metric_name, metric_value, metric_text, source) VALUES 
('2026-02-27', 'Commodities', 'Global PMI', 50.5, '50.5', 'S&P Global'),
('2026-02-27', 'Commodities', 'Crude Oil Price', 73.0, '$73.0/barrel', 'EIA');

-- Cross-Border Capital Flows & Carry Trade Risk
INSERT INTO market_data (date, category, metric_name, metric_value, metric_text, source) VALUES 
('2026-02-27', 'Capital Flows', 'USD-JPY Interest Rate Differential', 317, '317 bps', 'Central Banks'),
('2026-02-27', 'Capital Flows', 'TGA Balance', 680, '$680B', 'U.S. Treasury');

-- Extreme Liquidity Tightening Warning
INSERT INTO market_data (date, category, metric_name, metric_value, metric_text, source) VALUES 
('2026-02-27', 'Liquidity Risk', 'Cross-Asset Correlation Risk', 0, 'Low', 'Market Analysis'),
('2026-02-27', 'Liquidity Risk', 'Safe Haven Function', 1, 'Normal', 'Market Analysis');