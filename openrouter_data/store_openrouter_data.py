#!/usr/bin/env python3
"""
存储OpenRouter数据到数据库
"""

import sqlite3
import json
from datetime import datetime

def store_openrouter_data():
    """存储OpenRouter数据到数据库"""
    # 读取提取的数据
    with open('/home/admin/openclaw/workspace/openrouter_data/extracted_openrouter_data.json', 'r') as f:
        data = json.load(f)
    
    # 连接数据库
    conn = sqlite3.connect('/home/admin/openviking_workspace/database/market_report_data.db')
    cursor = conn.cursor()
    
    # 获取当前时间戳
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 存储通用排名数据
    for model in data['general_rankings']:
        cursor.execute("""
            INSERT OR REPLACE INTO openrouter_models 
            (model_name, provider, category, weekly_tokens, week_over_week_change, ranking_position, data_timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            model['model_name'],
            model['provider'],
            'general',
            model['weekly_tokens_billion'],
            model['week_over_week_change'],
            model['rank'],
            timestamp
        ))
    
    # 存储编程基准数据
    for model in data['coding_benchmark']:
        cursor.execute("""
            INSERT OR REPLACE INTO openrouter_models 
            (model_name, provider, category, weekly_tokens, week_over_week_change, ranking_position, data_timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            model['model_name'],
            model['provider'],
            'coding',
            model['weekly_tokens_billion'],
            model['week_over_week_change'],
            model['rank'],
            timestamp
        ))
    
    # 存储Top Apps数据
    for app in data['top_apps']:
        cursor.execute("""
            INSERT OR REPLACE INTO openrouter_apps 
            (app_name, app_url, weekly_tokens, ranking_position, data_timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (
            app['app_name'],
            app['app_url'],
            app['weekly_tokens_billion'],
            app['rank'],
            timestamp
        ))
    
    # 存储市场总数据
    cursor.execute("""
        INSERT OR REPLACE INTO openrouter_market_share 
        (provider, market_share_percentage, total_tokens, data_timestamp)
        VALUES (?, ?, ?, ?)
    """, (
        'total',
        100.0,
        data['monthly_total_tokens_trillion'],
        timestamp
    ))
    
    conn.commit()
    conn.close()
    
    print("✅ OpenRouter数据已成功存储到数据库！")

if __name__ == "__main__":
    store_openrouter_data()