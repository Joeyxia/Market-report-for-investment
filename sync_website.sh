#!/bin/bash
# 同步根目录的首页到 market-report-new 目录
cp index.html market-report-new/
# 确保 reports 目录同步
cp -r reports/* market-report-new/reports/
# 添加样式文件
cp style.css market-report-new/
echo "✅ Website files synchronized successfully!"