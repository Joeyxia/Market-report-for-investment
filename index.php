<?php
// 从数据库获取最新报告数据
$db = new SQLite3('/home/admin/openviking_workspace/database/market_report_data.db');

// 获取最新的5个报告
$reports = $db->query('SELECT report_date, overall_score, investment_signal FROM daily_reports ORDER BY report_date DESC LIMIT 5');

$reportList = [];
while ($row = $reports->fetchArray(SQLITE3_ASSOC)) {
    $reportList[] = $row;
}

// 生成HTML内容
ob_start();
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>市场报告 - 投资决策支持</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #ffffff;
            color: #333333;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 30px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-radius: 10px;
        }
        .header h1 {
            font-size: 32px;
            margin: 0 0 10px 0;
            font-weight: bold;
        }
        .header .subtitle {
            font-size: 24px;
            margin: 0;
            font-weight: bold;
        }
        .info-box {
            background: #f0f8f0;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #4CAF50;
        }
        .report-list {
            background: white;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .report-item {
            display: flex;
            justify-content: space-between;
            padding: 20px 0;
            border-bottom: 1px solid #eee;
            align-items: center;
        }
        .report-item:last-child {
            border-bottom: none;
        }
        .report-date {
            font-weight: bold;
            font-size: 18px;
            margin-bottom: 12px;
        }
        .report-link {
            color: #667eea;
            text-decoration: none;
            padding: 10px 20px;
            background: #f0f4ff;
            border-radius: 5px;
            font-weight: bold;
        }
        .report-link:hover {
            background: #667eea;
            color: white;
        }
        .score-badge {
            background: #ffd700;
            color: #333;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
            margin-right: 15px;
            margin-top: 10px;
            display: inline-block;
        }
        .signal-badge {
            background: #e8f4f8;
            color: #2196F3;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
            display: inline-block;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 14px;
        }
        @media (max-width: 768px) {
            .report-item {
                flex-direction: column;
                align-items: flex-start;
                gap: 15px;
            }
            .report-link {
                align-self: flex-end;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 市场报告</h1>
            <p class="subtitle">投资决策支持</p>
            <p style="margin-top: 15px; font-size: 16px;">基于11维度宏观经济模型的每日市场分析</p>
        </div>

        <div class="info-box">
            <strong>📈 报告更新时间：</strong>工作日 09:00 (中国时间) & 22:00 (北京时间)<br>
            <strong>🔍 数据来源：</strong>美国财政部、BLS、美联储等官方机构
        </div>

        <div class="report-list">
            <h2>📅 最新报告</h2>
            
            <?php foreach ($reportList as $report): ?>
            <div class="report-item">
                <div>
                    <div class="report-date"><?php echo $report['report_date']; ?></div>
                    <span class="score-badge">综合评分: <?php echo number_format($report['overall_score'], 1); ?>/100</span>
                    <span class="signal-badge">投资信号: <?php echo $report['investment_signal']; ?></span>
                </div>
                <a href="reports/<?php echo $report['report_date']; ?>_11d.html" class="report-link">查看报告</a>
            </div>
            <?php endforeach; ?>
        </div>

        <div class="report-list">
            <h2>📚 专业术语解释</h2>
            <div class="report-item">
                <div>
                    <div class="report-date">市场报告术语指南</div>
                    <p>SOFR、ERP、MOVE、TGA余额、日元套利交易等专业概念详解</p>
                </div>
                <a href="glossary.html" class="report-link">查看术语解释</a>
            </div>
        </div>

        <div class="report-list">
            <h2>📊 数据看板</h2>
            <div class="report-item">
                <div>
                    <div class="report-date">市场报告 & OpenViking记忆系统</div>
                    <p>实时数据统计和趋势分析</p>
                </div>
                <a href="dashboard/" class="report-link">查看数据看板</a>
            </div>
        </div>

        <div class="report-list">
            <h2>🤖 OpenRouter AI分析</h2>
            <div class="report-item">
                <div>
                    <div class="report-date">AI模型采用趋势分析</div>
                    <p>基于OpenRouter平台的AI Adoption深度洞察</p>
                </div>
                <a href="openrouter-analysis.html" class="report-link">查看AI分析</a>
            </div>
        </div>

        <div class="footer">
            <p>© 2026 市场报告 | 每日更新 | 基于11维度宏观经济模型</p>
        </div>
    </div>
</body>
</html>
<?php
echo ob_get_clean();
?>