"""
人流量预测器测试
"""

import unittest
from datetime import datetime
import sys
import os

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from predictors.traffic_predictor import TrafficPredictor
from models.prediction_models import RestaurantConfig, HistoricalData, PredictionContext


class TestTrafficPredictor(unittest.TestCase):
    """人流量预测器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.predictor = TrafficPredictor()
        
        # 创建测试用的餐厅配置
        self.restaurant_config = RestaurantConfig(
            restaurant_type='casual_dining',
            max_capacity=120,
            table_count=24,
            operating_hours=(11, 23),
            peak_hours=[12, 13, 18, 19, 20]
        )
        
        # 创建测试用的历史数据
        self.historical_data = HistoricalData(
            hourly_traffic={
                '2024-01-01': [2, 1, 1, 1, 2, 3, 5, 8, 12, 15, 20, 30, 40, 25, 15, 10, 8, 15, 35, 45, 30, 20, 12, 5],
                '2024-01-02': [3, 2, 1, 1, 2, 4, 6, 10, 15, 18, 25, 35, 45, 30, 18, 12, 10, 18, 40, 50, 35, 25, 15, 8]
            },
            daily_patterns={
                'monday': [2, 1, 1, 1, 2, 3, 5, 8, 12, 15, 20, 30, 40, 25, 15, 10, 8, 15, 35, 45, 30, 20, 12, 5],
                'tuesday': [3, 2, 1, 1, 2, 4, 6, 10, 15, 18, 25, 35, 45, 30, 18, 12, 10, 18, 40, 50, 35, 25, 15, 8]
            },
            weekly_patterns=[1.0, 0.9, 1.0, 1.1, 1.2, 1.5, 1.4],
            seasonal_factors={'spring': 1.0, 'summer': 1.3, 'autumn': 1.1, 'winter': 0.8},
            external_factors={'weather_impact': 0.15, 'holiday_impact': 0.4}
        )
        
        # 创建测试用的预测上下文
        self.context = PredictionContext(
            current_time=datetime.now(),
            weather_info={'temperature': 22, 'weather_type': 'cloudy'},
            is_holiday=False,
            local_events=['附近商场活动'],
            special_conditions=[]
        )
    
    def test_predictor_initialization(self):
        """测试预测器初始化"""
        self.assertEqual(self.predictor.name, "TrafficPredictor")
        self.assertFalse(self.predictor.is_trained)
        self.assertIsNotNone(self.predictor.default_patterns)
        
        # 测试默认模式包含所有餐厅类型
        self.assertIn('fast_food', self.predictor.default_patterns)
        self.assertIn('casual_dining', self.predictor.default_patterns)
        self.assertIn('fine_dining', self.predictor.default_patterns)
    
    def test_default_patterns_structure(self):
        """测试默认模式结构"""
        for restaurant_type, pattern in self.predictor.default_patterns.items():
            self.assertIn('peak_hours', pattern)
            self.assertIn('base_traffic', pattern)
            self.assertIn('weekend_multiplier', pattern)
            
            # 测试base_traffic有24小时数据
            self.assertEqual(len(pattern['base_traffic']), 24)
            
            # 测试weekend_multiplier是合理的数值
            self.assertGreater(pattern['weekend_multiplier'], 0.5)
            self.assertLess(pattern['weekend_multiplier'], 3.0)
    
    def test_train_method_signature(self):
        """测试训练方法签名"""
        self.assertTrue(hasattr(self.predictor, 'train'))
        self.assertTrue(callable(getattr(self.predictor, 'train')))
    
    def test_predict_method_signature(self):
        """测试预测方法签名"""
        self.assertTrue(hasattr(self.predictor, 'predict'))
        self.assertTrue(callable(getattr(self.predictor, 'predict')))
    
    def test_time_series_prediction_method(self):
        """测试时间序列预测方法"""
        self.assertTrue(hasattr(self.predictor, '_predict_with_time_series'))
        self.assertTrue(callable(getattr(self.predictor, '_predict_with_time_series')))
    
    def test_ml_prediction_method(self):
        """测试机器学习预测方法"""
        self.assertTrue(hasattr(self.predictor, '_predict_with_ml_model'))
        self.assertTrue(callable(getattr(self.predictor, '_predict_with_ml_model')))
    
    def test_cold_start_prediction_method(self):
        """测试冷启动预测方法"""
        self.assertTrue(hasattr(self.predictor, '_handle_cold_start_prediction'))
        self.assertTrue(callable(getattr(self.predictor, '_handle_cold_start_prediction')))
    
    def test_peak_identification_method(self):
        """测试高峰识别方法"""
        self.assertTrue(hasattr(self.predictor, '_identify_peak_periods'))
        self.assertTrue(callable(getattr(self.predictor, '_identify_peak_periods')))
    
    def test_confidence_intervals_method(self):
        """测试置信区间计算方法"""
        self.assertTrue(hasattr(self.predictor, '_calculate_confidence_intervals'))
        self.assertTrue(callable(getattr(self.predictor, '_calculate_confidence_intervals')))
    
    def test_chart_data_generation_method(self):
        """测试图表数据生成方法"""
        self.assertTrue(hasattr(self.predictor, '_generate_chart_data'))
        self.assertTrue(callable(getattr(self.predictor, '_generate_chart_data')))
    
    def test_external_factors_method(self):
        """测试外部因素应用方法"""
        self.assertTrue(hasattr(self.predictor, '_apply_external_factors'))
        self.assertTrue(callable(getattr(self.predictor, '_apply_external_factors')))
    
    def test_business_insights_method(self):
        """测试经营洞察方法"""
        self.assertTrue(hasattr(self.predictor, 'get_business_insights'))
        self.assertTrue(callable(getattr(self.predictor, 'get_business_insights')))
    
    def test_input_validation(self):
        """测试输入验证"""
        # 测试空输入
        self.assertFalse(self.predictor.validate_input({}))
        self.assertFalse(self.predictor.validate_input(None))
        
        # 测试有效输入
        valid_input = {
            'current_traffic': 25,
            'prediction_hours': 24,
            'restaurant_config': self.restaurant_config
        }
        self.assertTrue(self.predictor.validate_input(valid_input))


class TestTrafficPredictorIntegration(unittest.TestCase):
    """人流量预测器集成测试"""
    
    def setUp(self):
        """测试前准备"""
        self.predictor = TrafficPredictor()
    
    def test_restaurant_type_patterns(self):
        """测试不同餐厅类型的模式"""
        # 快餐店模式
        fast_food_pattern = self.predictor.default_patterns['fast_food']
        self.assertIn(12, fast_food_pattern['peak_hours'])  # 午餐高峰
        self.assertIn(18, fast_food_pattern['peak_hours'])  # 晚餐高峰
        
        # 精品餐厅模式
        fine_dining_pattern = self.predictor.default_patterns['fine_dining']
        self.assertIn(19, fine_dining_pattern['peak_hours'])  # 晚餐高峰较晚
        
        # 验证精品餐厅的周末倍数较小（相对稳定）
        self.assertLess(
            fine_dining_pattern['weekend_multiplier'],
            fast_food_pattern['weekend_multiplier']
        )
    
    def test_pattern_consistency(self):
        """测试模式一致性"""
        for restaurant_type, pattern in self.predictor.default_patterns.items():
            # 验证高峰时段的流量确实较高
            peak_hours = pattern['peak_hours']
            base_traffic = pattern['base_traffic']
            
            for peak_hour in peak_hours:
                if 0 <= peak_hour < 24:
                    # 高峰时段的流量应该高于平均值
                    avg_traffic = sum(base_traffic) / len(base_traffic)
                    self.assertGreaterEqual(
                        base_traffic[peak_hour], 
                        avg_traffic,
                        f"{restaurant_type}的{peak_hour}点流量应该高于平均值"
                    )


if __name__ == '__main__':
    unittest.main() 