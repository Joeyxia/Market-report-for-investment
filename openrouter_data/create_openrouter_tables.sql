-- 创建OpenRouter模型数据表
CREATE TABLE IF NOT EXISTS openrouter_models (
    model_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT NOT NULL,
    provider TEXT NOT NULL,
    category TEXT NOT NULL,
    weekly_tokens REAL,
    monthly_tokens REAL,
    week_over_week_change REAL,
    ranking_position INTEGER,
    data_timestamp DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建OpenRouter应用数据表
CREATE TABLE IF NOT EXISTS openrouter_apps (
    app_id INTEGER PRIMARY KEY AUTOINCREMENT,
    app_name TEXT NOT NULL,
    app_url TEXT,
    weekly_tokens REAL,
    ranking_position INTEGER,
    data_timestamp DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建OpenRouter市场份额数据表
CREATE TABLE IF NOT EXISTS openrouter_market_share (
    provider TEXT PRIMARY KEY,
    market_share_percentage REAL,
    total_tokens REAL,
    data_timestamp DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引以优化查询性能
CREATE INDEX IF NOT EXISTS idx_openrouter_models_category ON openrouter_models(category);
CREATE INDEX IF NOT EXISTS idx_openrouter_models_provider ON openrouter_models(provider);
CREATE INDEX IF NOT EXISTS idx_openrouter_models_timestamp ON openrouter_models(data_timestamp);
CREATE INDEX IF NOT EXISTS idx_openrouter_apps_timestamp ON openrouter_apps(data_timestamp);