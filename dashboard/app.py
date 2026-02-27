#!/usr/bin/env python3
"""
数据看板Flask应用
提供市场报告和OpenViking记忆系统的数据API
"""

from flask import Flask, jsonify, render_template
import sqlite3
import json
from datetime import datetime, timedelta

app = Flask(__name__)

def get_market_report_db():
    """获取市场报告数据库连接"""
    return sqlite3.connect('/home/admin/openviking_workspace/database/market_report_data.db')

def get_viking_memory_db():
    """获取OpenViking记忆数据库连接"""
    return sqlite3.connect('/home/admin/openviking_workspace/viking/viking_memory.db')

@app.route('/')
def dashboard():
    """数据看板主页"""
    return render_template('dashboard.html')

@app.route('/api/market-report/summary')
def market_report_summary():
    """获取市场报告摘要数据"""
    conn = get_market_report_db()
    cursor = conn.cursor()
    
    # 获取最近30天的报告数据
    cursor.execute("""
        SELECT report_date, overall_score, investment_signal 
        FROM daily_reports 
        ORDER BY report_date DESC 
        LIMIT 30
    """)
    reports = cursor.fetchall()
    
    # 获取最新维度分数
    if reports:
        latest_date = reports[0][0]
        cursor.execute("""
            SELECT dimension_name, score, weight, contribution 
            FROM dimension_scores 
            WHERE report_date = ? 
            ORDER BY dimension_id
        """, (latest_date,))
        dimensions = cursor.fetchall()
    else:
        dimensions = []
    
    # 获取关键指标
    cursor.execute("""
        SELECT metric_name, metric_value, verification_status 
        FROM key_metrics 
        WHERE report_date = (SELECT MAX(report_date) FROM daily_reports)
    """)
    metrics = cursor.fetchall()
    
    # 获取AI Token数据
    cursor.execute("""
        SELECT monthly_total_tokens_trillion, mom_growth_rate 
        FROM ai_token_data 
        WHERE report_date = (SELECT MAX(report_date) FROM daily_reports)
    """)
    ai_data = cursor.fetchone()
    
    conn.close()
    
    return jsonify({
        'reports': [
            {
                'date': report[0],
                'score': report[1],
                'signal': report[2]
            } for report in reports
        ],
        'dimensions': [
            {
                'name': dim[0],
                'score': dim[1],
                'weight': dim[2],
                'contribution': dim[3]
            } for dim in dimensions
        ],
        'metrics': [
            {
                'name': metric[0],
                'value': metric[1],
                'status': metric[2]
            } for metric in metrics
        ],
        'ai_data': {
            'monthly_tokens': ai_data[0] if ai_data else None,
            'mom_growth': ai_data[1] if ai_data else None
        }
    })

@app.route('/api/viking-memory/summary')
def viking_memory_summary():
    """获取OpenViking记忆系统摘要数据"""
    conn = get_viking_memory_db()
    cursor = conn.cursor()
    
    # 获取记忆总数
    cursor.execute("SELECT COUNT(*) FROM memories")
    total_memories = cursor.fetchone()[0]
    
    # 按分类统计
    cursor.execute("""
        SELECT category, COUNT(*) as count 
        FROM memories 
        GROUP BY category
    """)
    category_stats = cursor.fetchall()
    
    # 按优先级统计
    cursor.execute("""
        SELECT priority, COUNT(*) as count 
        FROM memories 
        GROUP BY priority
    """)
    priority_stats = cursor.fetchall()
    
    # 最近7天的记忆创建数量
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    cursor.execute("""
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM memories 
        WHERE created_at >= ?
        GROUP BY DATE(created_at)
        ORDER BY date
    """, (seven_days_ago,))
    recent_activity = cursor.fetchall()
    
    # 最近5个记忆
    cursor.execute("""
        SELECT memory_id, title, category, created_at 
        FROM memories 
        ORDER BY created_at DESC 
        LIMIT 5
    """)
    recent_memories = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'total_memories': total_memories,
        'category_stats': [
            {'category': stat[0], 'count': stat[1]} for stat in category_stats
        ],
        'priority_stats': [
            {'priority': stat[0], 'count': stat[1]} for stat in priority_stats
        ],
        'recent_activity': [
            {'date': activity[0], 'count': activity[1]} for activity in recent_activity
        ],
        'recent_memories': [
            {
                'id': memory[0],
                'title': memory[1],
                'category': memory[2],
                'created_at': memory[3]
            } for memory in recent_memories
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)