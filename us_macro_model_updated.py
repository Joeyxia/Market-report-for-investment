#!/usr/bin/env python3
"""
美股宏观投资模型 - 增强版 (包含资金流动性监控)
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
        self.indicators = {}
        
    def load_config(self, config_path):
        """加载指标配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"配置文件 {config_path} 未找到")
            return {}
    
    def get_indicator_data(self, indicator_key, category):
        """获取单个指标数据"""
        indicator = self.config[category][indicator_key]
        source = indicator['source']
        
        # 这里简化处理，实际应用中需要根据不同的数据源实现具体获取逻辑
        # 对于FRED数据源，可以使用API
        if 'fred.stlouisfed.org' in source:
            # FRED API 获取逻辑（简化版）
            return self._get_fred_data(indicator_key)
        else:
            # 其他数据源的处理逻辑
            return None
    
    def _get_fred_data(self, series_id):
        """从FRED获取数据（示例）"""
        # 实际实现需要FRED API密钥
        # 这里返回模拟数据
        return {
            'value': 4.5,  # 示例值
            'date': datetime.now().strftime('%Y-%m-%d'),
            'change': 0.1
        }
    
    def collect_all_indicators(self):
        """收集所有指标数据"""
        all_categories = ['monetary_policy', 'economic_growth', 
                         'market_sentiment', 'commodities', 'liquidity']
        
        for category in all_categories:
            if category in self.config:
                for indicator_key in self.config[category]:
                    data = self.get_indicator_data(indicator_key, category)
                    if data:
                        self.indicators[f"{category}.{indicator_key}"] = data
        
        return self.indicators
    
    def analyze_liquidity_conditions(self):
        """分析市场资金流动性状况"""
        liquidity_score = 0
        liquidity_analysis = []
        
        # 检查M2货币供应量
        if 'liquidity.m2_money_supply' in self.indicators:
            m2_data = self.indicators['liquidity.m2_money_supply']
            if m2_data['change'] > 0:
                liquidity_score += 1
                liquidity_analysis.append("✅ M2货币供应量增长，流动性充裕")
            else:
                liquidity_score -= 1
                liquidity_analysis.append("⚠️ M2货币供应量收缩，流动性紧张")
        
        # 检查美联储资产负债表
        if 'liquidity.fed_balance_sheet' in self.indicators:
            fed_bs_data = self.indicators['liquidity.fed_balance_sheet']
            if fed_bs_data['change'] < 0:  # 缩表
                liquidity_score -= 1
                liquidity_analysis.append("⚠️ 美联储缩表，流动性收紧")
            else:
                liquidity_score += 1
                liquidity_analysis.append("✅ 美联储扩表或稳定，流动性支持")
        
        # 检查TED利差
        if 'liquidity.ted_spread' in self.indicators:
            ted_data = self.indicators['liquidity.ted_spread']
            if ted_data['value'] > 0.5:  # 50基点以上
                liquidity_score -= 2
                liquidity_analysis.append("🚨 TED利差扩大，银行间流动性紧张")
            elif ted_data['value'] > 0.3:
                liquidity_score -= 1
                liquidity_analysis.append("⚠️ TED利差偏高，流动性略有压力")
            else:
                liquidity_score += 1
                liquidity_analysis.append("✅ TED利差正常，银行间流动性良好")
        
        # 检查商业票据利差
        if 'liquidity.commercial_paper_spread' in self.indicators:
            cp_data = self.indicators['liquidity.commercial_paper_spread']
            if cp_data['value'] > 1.0:  # 100基点以上
                liquidity_score -= 1
                liquidity_analysis.append("⚠️ 商业票据利差扩大，企业融资成本上升")
            else:
                liquidity_score += 1
                liquidity_analysis.append("✅ 商业票据利差正常，企业融资环境良好")
        
        # 检查逆回购规模
        if 'liquidity.reverse_repo' in self.indicators:
            rr_data = self.indicators['liquidity.reverse_repo']
            if rr_data['value'] > 2000:  # 2000亿美元以上
                liquidity_score -= 1
                liquidity_analysis.append("⚠️ 逆回购规模高企，市场流动性过剩但可能反映避险情绪")
            else:
                liquidity_score += 1
                liquidity_analysis.append("✅ 逆回购规模适中，流动性分布合理")
        
        return {
            'score': liquidity_score,
            'analysis': liquidity_analysis,
            'status': self._get_liquidity_status(liquidity_score)
        }
    
    def _get_liquidity_status(self, score):
        """根据分数判断流动性状态"""
        if score >= 3:
            return "充裕"
        elif score >= 1:
            return "适中"
        elif score >= -1:
            return "偏紧"
        else:
            return "紧张"
    
    def generate_investment_signal(self):
        """生成综合投资信号"""
        # 收集所有指标
        self.collect_all_indicators()
        
        # 分析流动性
        liquidity_result = self.analyze_liquidity_conditions()
        
        # 这里可以添加其他维度的分析（货币政策、经济数据等）
        # 为简化，主要基于流动性分析
        
        signal = {
            'timestamp': datetime.now().isoformat(),
            'liquidity_status': liquidity_result['status'],
            'liquidity_score': liquidity_result['score'],
            'liquidity_analysis': liquidity_result['analysis'],
            'recommendation': self._generate_recommendation(liquidity_result['status'])
        }
        
        return signal
    
    def _generate_recommendation(self, liquidity_status):
        """基于流动性状态生成投资建议"""
        recommendations = {
            '充裕': '📈 流动性充裕，可适当增加风险资产配置，关注成长股和小盘股',
            '适中': '📊 流动性适中，维持均衡配置，关注盈利确定性强的优质公司',
            '偏紧': '⚠️ 流动性偏紧，降低仓位至60-70%，增加现金和防御性资产',
            '紧张': '📉 流动性紧张，大幅降低风险敞口至40%以下，重点关注高股息和必需消费品'
        }
        return recommendations.get(liquidity_status, '📊 维持当前配置，密切监控流动性变化')

def main():
    """主函数 - 用于测试"""
    model = USMacroModel()
    signal = model.generate_investment_signal()
    
    print("=== 美股宏观投资模型信号 ===")
    print(f"时间: {signal['timestamp']}")
    print(f"流动性状态: {signal['liquidity_status']} (评分: {signal['liquidity_score']})")
    print("\n流动性分析:")
    for analysis in signal['liquidity_analysis']:
        print(f"  {analysis}")
    print(f"\n投资建议: {signal['recommendation']}")

if __name__ == "__main__":
    main()