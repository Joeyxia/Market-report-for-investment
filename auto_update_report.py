#!/usr/bin/env python3
"""
自动更新市场报告网站的脚本
- 生成每日报告HTML
- 更新首页索引
- 自动推送到GitHub
"""

import os
import json
import datetime
from pathlib import Path

def generate_daily_report_html(date_str, report_data):
    """生成单日报告HTML页面"""
    template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>宏观经济模型报告 - {date_str}</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 宏观经济模型报告</h1>
            <div class="date">{date_str}</div>
            <div class="score">综合评分: {report_data.get('score', '54.6')}/100</div>
            <div class="signal">投资信号: {report_data.get('signal', '中性偏谨慎')}</div>
        </div>
        
        <!-- 报告内容将由AI生成并填充 -->
        <div class="conclusion">
            <h2>🚨 核心结论</h2>
            <p>{report_data.get('conclusion', '基于最新数据的分析...')}</p>
        </div>
        
        <div class="footer">
            <p><a href="../index.html">← 返回首页</a></p>
            <p>数据来源: 美国财政部、BLS等官方机构 + 最新市场数据</p>
        </div>
    </div>
</body>
</html>"""
    return template

def update_homepage_index():
    """更新首页，包含所有报告链接"""
    reports_dir = Path("reports")
    if not reports_dir.exists():
        reports_dir.mkdir()
    
    # 获取所有报告文件
    report_files = list(reports_dir.glob("*.html"))
    report_files.sort(reverse=True)  # 按日期倒序排列
    
    links_html = ""
    for report_file in report_files:
        date_str = report_file.stem  # 移除.html后缀
        links_html += f'        <li><a href="reports/{report_file.name}">{date_str}</a></li>\n'
    
    homepage_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>宏观经济模型报告</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>宏观经济模型报告</h1>
            <p>每日宏观经济分析与投资建议</p>
        </div>
        
        <div class="reports-list">
            <h2>📈 历史报告</h2>
            <ul>
{links_html}
            </ul>
        </div>
        
        <div class="footer">
            <p>自动更新于 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>"""
    
    return homepage_template

def main():
    """主函数：生成报告并更新网站"""
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    # 这里会调用AI生成实际的报告数据
    # 目前先使用占位符
    report_data = {
        "score": "54.6",
        "signal": "中性偏谨慎", 
        "conclusion": "基于最新数据的分析..."
    }
    
    # 生成今日报告
    report_html = generate_daily_report_html(today, report_data)
    with open(f"reports/{today}.html", "w", encoding="utf-8") as f:
        f.write(report_html)
    
    # 更新首页
    homepage_html = update_homepage_index()
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(homepage_html)
    
    print(f"✅ 已生成报告: reports/{today}.html")
    print("✅ 已更新首页: index.html")

if __name__ == "__main__":
    main()