#!/usr/bin/env python3
"""
美股宏观指标监控脚本 - 包含市场资金流动性监控
支持每日报告和实时警报功能
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
        try:
            # 这里应该实现实际的数据获取逻辑
            # 由于网络限制，暂时返回模拟数据
            source = indicator_config.get('source', '')
            frequency = indicator_config.get('frequency', 'daily')
            
            # 模拟数据获取
            if 'federal_funds_rate' in indicator_name:
                return {'value': 5.25, 'change': 0.0, 'timestamp': datetime.now().isoformat()}
            elif 'treasury_10y' in indicator_name:
                return {'value': 4.35, 'change': -0.02, 'timestamp': datetime.now().isoformat()}
            elif 'm2_money_supply' in indicator_name:
                return {'value': 20800, 'change': -0.5, 'timestamp': datetime.now().isoformat()}
            elif 'fed_balance_sheet' in indicator_name:
                return {'value': 7400, 'change': -10, 'timestamp': datetime.now().isoformat()}
            elif 'repo_market' in indicator_name:
                return {'value': 5.30, 'change': 0.05, 'timestamp': datetime.now().isoformat()}
            elif 'commercial_paper' in indicator_name:
                return {'value': 5.45, 'change': 0.10, 'timestamp': datetime.now().isoformat()}
            elif 'vix_index' in indicator_name:
                return {'value': 18.5, 'change': 2.3, 'timestamp': datetime.now().isoformat()}
            else:
                return {'value': 100.0, 'change': 0.0, 'timestamp': datetime.now().isoformat()}
                
        except Exception as e:
            logger.error(f"获取指标 {indicator_name} 数据失败: {e}")
            return None
    
    def check_liquidity_alerts(self, liquidity_data):
        """检查流动性相关警报"""
        alerts = []
        
        # M2货币供应量异常收缩
        if 'm2_money_supply' in liquidity_data:
            m2_change = liquidity_data['m2_money_supply'].get('change', 0)
            if m2_change < -2.0:  # 月度收缩超过2%
                alerts.append("🚨 M2货币供应量大幅收缩，流动性紧张风险上升")
        
        # 美联储资产负债表快速缩减
        if 'fed_balance_sheet' in liquidity_data:
            balance_change = liquidity_data['fed_balance_sheet'].get('change', 0)
            if balance_change < -50:  # 单周缩减超过500亿美元
                alerts.append("🚨 美联储资产负债表快速缩减，市场流动性承压")
        
        # 回购市场利率飙升
        if 'repo_market' in liquidity_data:
            repo_rate = liquidity_data['repo_market'].get('value', 0)
            repo_change = liquidity_data['repo_market'].get('change', 0)
            if repo_rate > 6.0 or repo_change > 0.5:
                alerts.append("🚨 回购市场利率飙升，短期流动性出现压力")
        
        # 商业票据利差扩大
        if 'commercial_paper' in liquidity_data:
            cp_rate = liquidity_data['commercial_paper'].get('value', 0)
            treasury_10y = liquidity_data.get('treasury_10y', {}).get('value', 4.0)
            cp_spread = cp_rate - treasury_10y
            if cp_spread > 2.0:  # 利差超过200基点
                alerts.append("🚨 商业票据与国债利差扩大，信用市场流动性紧张")
        
        return alerts
    
    def generate_daily_report(self):
        """生成每日宏观报告"""
        report = []
        report.append("📊 **美股宏观指标每日报告**")
        report.append(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("")
        
        # 获取所有指标数据
        all_data = {}
        for category, indicators in self.indicators.items():
            for indicator_name, config in indicators.items():
                data = self.fetch_indicator_data(indicator_name, config)
                if data:
                    all_data[indicator_name] = data
        
        # 货币政策部分
        report.append("🏦 **货币政策**")
        if 'federal_funds_rate' in all_data:
            ff_data = all_data['federal_funds_rate']
            report.append(f"• 联邦基金利率: {ff_data['value']:.2f}%")
        if 'treasury_10y' in all_data:
            t10_data = all_data['treasury_10y']
            report.append(f"• 10年期国债收益率: {t10_data['value']:.2f}% (变化: {t10_data['change']:+.2f}%)")
        report.append("")
        
        # 市场流动性部分（新增）
        report.append("💧 **市场资金流动性**")
        liquidity_indicators = ['m2_money_supply', 'fed_balance_sheet', 'repo_market', 'commercial_paper']
        liquidity_data = {}
        for liq_ind in liquidity_indicators:
            if liq_ind in all_data:
                liquidity_data[liq_ind] = all_data[liq_ind]
                if liq_ind == 'm2_money_supply':
                    report.append(f"• M2货币供应量: ${all_data[liq_ind]['value']:.0f}B (月度变化: {all_data[liq_ind]['change']:+.1f}%)")
                elif liq_ind == 'fed_balance_sheet':
                    report.append(f"• 美联储资产负债表: ${all_data[liq_ind]['value']:.0f}B (周度变化: {all_data[liq_ind]['change']:+.0f}B)")
                elif liq_ind == 'repo_market':
                    report.append(f"• 回购市场利率: {all_data[liq_ind]['value']:.2f}% (变化: {all_data[liq_ind]['change']:+.2f}%)")
                elif liq_ind == 'commercial_paper':
                    report.append(f"• 商业票据利率: {all_data[liq_ind]['value']:.2f}%")
        report.append("")
        
        # 流动性警报检查
        liquidity_alerts = self.check_liquidity_alerts(all_data)
        if liquidity_alerts:
            report.append("⚠️ **流动性风险警报**")
            for alert in liquidity_alerts:
                report.append(f"• {alert}")
            report.append("")
        
        # 投资信号
        report.append("🎯 **综合投资信号**")
        report.append("基于当前宏观环境，建议:")
        report.append("• 密切关注流动性指标变化")
        report.append("• M2收缩和资产负债表缩减可能对市场构成压力")
        report.append("• 回购市场和商业票据利差是短期流动性的重要观察窗口")
        
        return "\n".join(report)
    
    def check_real_time_alerts(self):
        """检查实时警报"""
        alerts = []
        
        # 获取最新数据
        all_data = {}
        for category, indicators in self.indicators.items():
            for indicator_name, config in indicators.items():
                data = self.fetch_indicator_data(indicator_name, config)
                if data:
                    all_data[indicator_name] = data
        
        # 检查流动性警报
        liquidity_alerts = self.check_liquidity_alerts(all_data)
        alerts.extend(liquidity_alerts)
        
        # 其他重要警报
        if 'vix_index' in all_data:
            vix_data = all_data['vix_index']
            if vix_data.get('value', 0) > 30 or vix_data.get('change', 0) > 5:
                alerts.append("🚨 VIX恐慌指数激增，市场波动性急剧上升")
        
        return alerts

def main():
    monitor = MacroMonitor()
    
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == '--status':
            # 生成状态报告
            report = monitor.generate_daily_report()
            print(report)
        elif sys.argv[1] == '--alerts':
            # 检查实时警报
            alerts = monitor.check_real_time_alerts()
            if alerts:
                print("🚨 **实时警报**")
                for alert in alerts:
                    print(alert)
            else:
                print("✅ 无异常警报")
    else:
        print("Usage: python monitor_macro.py [--status | --alerts]")

if __name__ == "__main__":
    main()