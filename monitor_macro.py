#!/usr/bin/env python3
"""
美股宏观指标监控脚本 - 包含流动性监控
支持每日报告和实时警报
"""

import json
import requests
import time
from datetime import datetime, timedelta
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MacroMonitor:
    def __init__(self):
        self.config_file = "macro_indicators.json"
        self.alert_config = "macro_alert_config.json"
        self.indicators = self.load_config()
        self.alerts = self.load_alert_config()
        
    def load_config(self):
        """加载宏观指标配置"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"配置文件 {self.config_file} 未找到")
            return {}
            
    def load_alert_config(self):
        """加载警报配置"""
        try:
            with open(self.alert_config, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"警报配置文件 {self.alert_config} 未找到")
            return {}
    
    def fetch_indicator_data(self, indicator_name, indicator_config):
        """获取单个指标数据"""
        source = indicator_config.get('source')
        if not source:
            return None
            
        try:
            # 这里是简化版本，实际实现需要根据数据源类型处理
            # FRED API, Yahoo Finance, 或其他金融数据API
            logger.info(f"获取指标 {indicator_name}: {indicator_config['name']}")
            
            # 模拟数据获取（实际使用时需要替换为真实API调用）
            if 'fred.stlouisfed.org' in source:
                # FRED API 调用示例
                return self.fetch_fred_data(indicator_name)
            elif 'yahoo' in source or 'market' in source:
                # Yahoo Finance 或市场数据API
                return self.fetch_market_data(indicator_name)
            else:
                # 其他数据源
                return {"value": "N/A", "timestamp": datetime.now().isoformat()}
                
        except Exception as e:
            logger.error(f"获取指标 {indicator_name} 失败: {e}")
            return None
    
    def fetch_fred_data(self, series_id):
        """从FRED获取数据（需要API密钥）"""
        # 实际实现需要FRED API密钥
        # 这里返回模拟数据
        fake_values = {
            'federal_funds_rate': 5.25,
            'treasury_10y': 4.3,
            'dxy_index': 104.5,
            'cpi_us': 3.1,
            'gdp_us': 2.1,
            'nonfarm_payrolls': 200000,
            'unemployment_rate': 3.7,
            'vix_index': 15.2,
            'wti_oil': 75.3,
            'gold_price': 2050.5
        }
        return {
            "value": fake_values.get(series_id, "N/A"),
            "timestamp": datetime.now().isoformat()
        }
    
    def fetch_market_data(self, indicator_name):
        """从市场数据源获取数据"""
        # 流动性指标的模拟数据
        liquidity_values = {
            'm2_money_supply': 20800.0,  # 十亿美元
            'fed_balance_sheet': 7500.0,  # 十亿美元  
            'repo_rate': 5.3,
            'commercial_paper_spread': 0.15,
            'high_yield_spread': 3.8,
            'investment_grade_spread': 1.2,
            'ted_spread': 0.35,
            'libor_3m': 5.25,
            'corporate_bond_fund_flows': 1200.0,  # 百万美元
            'equity_fund_flows': -800.0,  # 百万美元
            'margin_debt': 650.0,  # 十亿美元
            'nyse_trading_volume': 4.2,  # 十亿股
            'put_call_ratio': 0.85,
            'advance_decline_line': 12500,
            'money_market_fund_assets': 5800.0,  # 十亿美元
            'bank_reserves': 3200.0,  # 十亿美元
            'term_premium_10y': 0.8,
            'yield_curve_2s10s': -0.45,  # 2年-10年利差
            'credit_card_delinquency': 2.8,
            'loan_growth_yoy': 3.2
        }
        return {
            "value": liquidity_values.get(indicator_name, "N/A"),
            "timestamp": datetime.now().isoformat()
        }
    
    def check_liquidity_alerts(self, liquidity_data):
        """检查流动性相关警报"""
        alerts = []
        
        # 关键流动性警报条件
        if liquidity_data.get('m2_money_supply'):
            # M2货币供应量大幅收缩
            if liquidity_data['m2_money_supply'] < 20000:  # 示例阈值
                alerts.append("⚠️ M2货币供应量低于20万亿美元，流动性紧张")
                
        if liquidity_data.get('fed_balance_sheet'):
            # 美联储资产负债表快速收缩
            if liquidity_data['fed_balance_sheet'] < 7000:  # 示例阈值
                alerts.append("⚠️ 美联储资产负债表低于7万亿美元，量化紧缩影响")
                
        if liquidity_data.get('high_yield_spread'):
            # 高收益债利差扩大
            if liquidity_data['high_yield_spread'] > 5.0:
                alerts.append("🚨 高收益债利差超过500基点，信用风险上升")
                
        if liquidity_data.get('yield_curve_2s10s'):
            # 收益率曲线倒挂加深
            if liquidity_data['yield_curve_2s10s'] < -1.0:
                alerts.append("🚨 2年-10年收益率曲线倒挂超过100基点，衰退风险高")
                
        if liquidity_data.get('margin_debt'):
            # 保证金债务激增
            if liquidity_data['margin_debt'] > 700:
                alerts.append("⚠️ 保证金债务超过7000亿美元，杠杆风险增加")
                
        return alerts
    
    def generate_daily_report(self):
        """生成每日宏观报告"""
        report = []
        report.append("📊 **美股宏观指标每日报告**")
        report.append(f"📅 日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("")
        
        # 货币政策
        report.append("### 💰 货币政策指标")
        for name, config in self.indicators.get('monetary_policy', {}).items():
            data = self.fetch_indicator_data(name, config)
            if data:
                report.append(f"- {config['name']}: {data['value']}")
        report.append("")
        
        # 经济增长
        report.append("### 📈 经济增长指标")
        for name, config in self.indicators.get('economic_growth', {}).items():
            data = self.fetch_indicator_data(name, config)
            if data:
                report.append(f"- {config['name']}: {data['value']}")
        report.append("")
        
        # 市场情绪
        report.append("### 😊 市场情绪指标")
        for name, config in self.indicators.get('market_sentiment', {}).items():
            data = self.fetch_indicator_data(name, config)
            if data:
                report.append(f"- {config['name']}: {data['value']}")
        report.append("")
        
        # 大宗商品
        report.append("### ⛽ 大宗商品指标")
        for name, config in self.indicators.get('commodities', {}).items():
            data = self.fetch_indicator_data(name, config)
            if data:
                report.append(f"- {config['name']}: {data['value']}")
        report.append("")
        
        # 💧 新增：市场流动性指标
        report.append("### 💧 市场流动性指标")
        for name, config in self.indicators.get('market_liquidity', {}).items():
            data = self.fetch_indicator_data(name, config)
            if data:
                report.append(f"- {config['name']}: {data['value']}")
        report.append("")
        
        # 流动性警报检查
        liquidity_data = {}
        for name, config in self.indicators.get('market_liquidity', {}).items():
            data = self.fetch_indicator_data(name, config)
            if data and data['value'] != "N/A":
                liquidity_data[name] = data['value']
                
        liquidity_alerts = self.check_liquidity_alerts(liquidity_data)
        if liquidity_alerts:
            report.append("### 🚨 流动性风险警报")
            for alert in liquidity_alerts:
                report.append(f"- {alert}")
            report.append("")
        
        # 投资信号
        signal = self.generate_investment_signal()
        report.append(f"### 🎯 投资信号: {signal}")
        
        return "\n".join(report)
    
    def generate_investment_signal(self):
        """生成投资信号（简化版）"""
        # 实际实现需要更复杂的逻辑
        return "【谨慎乐观】关注流动性变化和美联储政策转向"
    
    def run_scheduled_check(self):
        """运行定时检查"""
        logger.info("开始执行宏观指标检查...")
        report = self.generate_daily_report()
        print(report)
        return report

def main():
    monitor = MacroMonitor()
    
    # 检查命令行参数
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == '--status':
            # 生成状态报告
            monitor.run_scheduled_check()
        elif sys.argv[1] == '--alerts':
            # 只检查警报
            liquidity_data = {}
            for name, config in monitor.indicators.get('market_liquidity', {}).items():
                data = monitor.fetch_indicator_data(name, config)
                if data and data['value'] != "N/A":
                    liquidity_data[name] = data['value']
            alerts = monitor.check_liquidity_alerts(liquidity_data)
            if alerts:
                print("🚨 流动性警报:")
                for alert in alerts:
                    print(f"- {alert}")
            else:
                print("✅ 无流动性风险警报")
    else:
        # 默认生成完整报告
        monitor.run_scheduled_check()

if __name__ == "__main__":
    main()