#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
美股宏观投资模型 - 包含市场资金流动性监控
"""

import json
import requests
from datetime import datetime, timedelta
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class USMacroModel:
    def __init__(self, config_path="macro_indicators.json"):
        """初始化宏观模型"""
        self.config = self.load_config(config_path)
        self.liquidity_weight = 0.3  # 流动性指标权重
        self.monetary_weight = 0.25  # 货币政策权重  
        self.economic_weight = 0.25  # 经济数据权重
        self.sentiment_weight = 0.15  # 市场情绪权重
        self.commodity_weight = 0.05  # 大宗商品权重
        
    def load_config(self, config_path):
        """加载指标配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"配置文件 {config_path} 未找到")
            return {}
    
    def get_fed_balance_sheet(self):
        """获取美联储资产负债表数据（万亿美金）"""
        # 模拟数据 - 实际应从FRED API获取
        return {
            "current": 7.4,
            "previous": 7.5,
            "change": -0.1,
            "trend": "收缩"
        }
    
    def get_m2_money_supply(self):
        """获取M2货币供应量（万亿美金）"""
        # 模拟数据 - 实际应从FRED API获取  
        return {
            "current": 20.8,
            "yoy_change": -1.2,  # 同比变化%
            "trend": "收缩"
        }
    
    def get_repo_market_rates(self):
        """获取回购市场利率"""
        # 模拟数据 - 实际应从市场数据源获取
        return {
            "sofr": 5.32,
            "secured_overnight": 5.30,
            "stress_level": "低"
        }
    
    def get_etf_flows(self):
        """获取ETF资金流向（十亿美元）"""
        # 模拟数据 - 实际应从ETF提供商API获取
        return {
            "sp500_etf_inflow": 2.1,
            "bond_etf_outflow": -1.8,
            "net_equity_flow": "正向"
        }
    
    def get_margin_debt(self):
        """获取保证金债务水平"""
        # 模拟数据 - 实际应从FINRA获取
        return {
            "current_billion": 620,
            "change_from_peak": -15,
            "risk_level": "中等"
        }
    
    def calculate_liquidity_score(self):
        """计算市场流动性综合评分 (0-100)"""
        # 获取各流动性指标
        balance_sheet = self.get_fed_balance_sheet()
        m2_supply = self.get_m2_money_supply() 
        repo_rates = self.get_repo_market_rates()
        etf_flows = self.get_etf_flows()
        margin_debt = self.get_margin_debt()
        
        # 计算流动性评分
        score = 50  # 基准分
        
        # 美联储资产负债表趋势
        if balance_sheet["trend"] == "扩张":
            score += 10
        elif balance_sheet["trend"] == "收缩":
            score -= 8
            
        # M2货币供应量同比变化
        if m2_supply["yoy_change"] > 0:
            score += 8
        elif m2_supply["yoy_change"] < -2:
            score -= 10
            
        # 回购市场压力水平
        if repo_rates["stress_level"] == "低":
            score += 5
        elif repo_rates["stress_level"] == "高":
            score -= 12
            
        # ETF资金流向
        if etf_flows["net_equity_flow"] == "正向":
            score += 7
        else:
            score -= 5
            
        # 保证金债务风险
        if margin_debt["risk_level"] == "低":
            score += 5
        elif margin_debt["risk_level"] == "高":
            score -= 8
            
        return max(0, min(100, score))
    
    def get_liquidity_status(self):
        """获取流动性状态描述"""
        score = self.calculate_liquidity_score()
        
        if score >= 70:
            return "充裕", "市场资金流动性充足，有利于风险资产"
        elif score >= 50:
            return "中性", "市场资金流动性适中，需关注变化趋势"
        elif score >= 30:
            return "紧张", "市场资金流动性偏紧，可能压制风险偏好"
        else:
            return "枯竭", "市场资金流动性严重不足，高风险环境"
    
    def generate_macro_signal(self):
        """生成宏观投资信号"""
        liquidity_status, liquidity_desc = self.get_liquidity_status()
        liquidity_score = self.calculate_liquidity_score()
        
        # 其他指标评分（简化版）
        monetary_score = 55  # 货币政策评分
        economic_score = 60  # 经济数据评分  
        sentiment_score = 45  # 市场情绪评分
        commodity_score = 50  # 大宗商品评分
        
        # 综合评分
        composite_score = (
            liquidity_score * self.liquidity_weight +
            monetary_score * self.monetary_weight +
            economic_score * self.economic_weight +
            sentiment_score * self.sentiment_weight +
            commodity_score * self.commodity_weight
        )
        
        # 生成信号
        if composite_score >= 65:
            signal = "看涨"
            recommendation = "增加股票仓位，关注成长股"
        elif composite_score >= 45:
            signal = "中性"
            recommendation = "维持现有仓位，精选个股"
        else:
            signal = "看跌"
            recommendation = "降低股票仓位，增加现金和债券"
            
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "composite_score": round(composite_score, 1),
            "signal": signal,
            "recommendation": recommendation,
            "liquidity": {
                "status": liquidity_status,
                "score": liquidity_score,
                "description": liquidity_desc
            },
            "component_scores": {
                "liquidity": liquidity_score,
                "monetary": monetary_score,
                "economic": economic_score,
                "sentiment": sentiment_score,
                "commodity": commodity_score
            }
        }
    
    def get_liquidity_alerts(self):
        """检查流动性相关警报"""
        alerts = []
        
        # 检查美联储资产负债表快速收缩
        balance_sheet = self.get_fed_balance_sheet()
        if balance_sheet["change"] < -0.5:
            alerts.append("⚠️ 美联储资产负债表快速收缩")
            
        # 检查M2货币供应量大幅下降
        m2_supply = self.get_m2_money_supply()
        if m2_supply["yoy_change"] < -3:
            alerts.append("⚠️ M2货币供应量同比大幅下降")
            
        # 检查回购市场压力
        repo_rates = self.get_repo_market_rates()
        if repo_rates["stress_level"] == "高":
            alerts.append("⚠️ 回购市场出现流动性压力")
            
        # 检查ETF大幅流出
        etf_flows = self.get_etf_flows()
        if etf_flows["net_equity_flow"] == "负向" and abs(etf_flows["sp500_etf_inflow"]) > 5:
            alerts.append("⚠️ 股票ETF出现大幅资金流出")
            
        return alerts

# 使用示例
if __name__ == "__main__":
    model = USMacroModel()
    signal = model.generate_macro_signal()
    alerts = model.get_liquidity_alerts()
    
    print("📊 美股宏观投资模型信号")
    print(f"⏰ 时间: {signal['timestamp']}")
    print(f"📈 综合评分: {signal['composite_score']}/100")
    print(f"🎯 投资信号: {signal['signal']}")
    print(f"💡 建议: {signal['recommendation']}")
    print(f"\n💧 流动性状态: {signal['liquidity']['status']}")
    print(f"   描述: {signal['liquidity']['description']}")
    
    if alerts:
        print(f"\n🚨 流动性警报:")
        for alert in alerts:
            print(f"   {alert}")