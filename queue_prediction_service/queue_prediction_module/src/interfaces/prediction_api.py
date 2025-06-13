"""
餐厅排队预测系统 - 预测API接口
提供统一的预测服务接口，供其他系统调用
"""

from typing import Dict, Any, Optional
from datetime import datetime
from ..predictors.wait_time_predictor import WaitTimePredictor
from ..predictors.traffic_predictor import TrafficPredictor
from ..algorithms.queue_theory import QueueTheoryCalculator
from ..algorithms.time_series_analysis import TimeSeriesAnalyzer
from ..models.prediction_models import (
    QueueData, RestaurantConfig, HistoricalData, 
    PredictionContext, WaitTimePrediction, TrafficPrediction
)


class PredictionAPIError(Exception):
    """预测API异常"""
    pass


class PredictionAPI:
    """
    预测API服务类
    
    提供统一的预测服务接口：
    1. 等待时间预测服务
    2. 人流量预测服务
    3. 时间序列分析服务
    """
    
    def __init__(self):
        """初始化预测API服务"""
        self.wait_time_predictor = WaitTimePredictor()
        self.traffic_predictor = TrafficPredictor()
        self.queue_calculator = QueueTheoryCalculator()
        self.time_series_analyzer = TimeSeriesAnalyzer()
        self.is_initialized = False
        self.last_training_time = None
        self.prediction_cache = {}
    
    def predict_wait_time(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        统一的等待时间预测接口
        
        Args:
            params: 参数字典
                - method: 预测方法 ('mm1', 'mmc', 'position')
                - arrival_rate: 到达率 (顾客/小时)
                - service_rate: 服务率 (顾客/小时)
                - servers: 服务台数量 (mmc方法需要)
                - current_queue_length: 当前排队人数 (position方法需要)
                - customer_position: 顾客位置 (position方法需要)
                
        Returns:
            Dict[str, Any]: 预测结果
                - avg_wait_time: 平均等待时间(分钟)
                - avg_system_time: 平均系统时间(分钟)
                - utilization: 系统利用率
                - avg_queue_length: 平均队列长度
                - prob_wait: 需要等待的概率 (仅mmc方法)
                
        Raises:
            PredictionAPIError: 预测失败时抛出
        """
        try:
            method = params.get('method', 'mm1')
            if method == 'mm1':
                result = self.queue_calculator.calculate_mm1_wait_time(
                    params['arrival_rate'],
                    params['service_rate']
                )
            elif method == 'mmc':
                result = self.queue_calculator.calculate_mmc_wait_time(
                    params['arrival_rate'],
                    params['service_rate'],
                    params['servers']
                )
            elif method == 'position':
                result = self.queue_calculator.calculate_customer_position_wait_time(
                    params['current_queue_length'],
                    params['customer_position'],
                    params['service_rate'],
                    params['servers']
                )
                # 将单个等待时间转换为标准格式
                result = {
                    'avg_wait_time': result,
                    'avg_system_time': result + (60 / params['service_rate']),
                    'utilization': params['current_queue_length'] / params['servers'],
                    'avg_queue_length': params['current_queue_length']
                }
            else:
                raise PredictionAPIError(f"Unknown method: {method}")
            
            # 转换为可序列化的格式
            return {k: float(v) if isinstance(v, (int, float)) else v 
                    for k, v in result.items()}
                    
        except Exception as e:
            raise PredictionAPIError(f"等待时间预测失败: {str(e)}")
    
    def predict_traffic(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        统一的人流量预测接口
        
        Args:
            params: 参数字典
                - current_traffic: 当前人流量
                - prediction_hours: 预测时长(小时)
                - restaurant_config: 餐厅配置信息
                - context: 预测上下文信息
                
        Returns:
            Dict[str, Any]: 预测结果
                - time_slots: 时间段列表
                - predicted_traffic: 预测人流量列表
                - confidence_intervals: 置信区间
                - peak_periods: 高峰时段信息
                - chart_data: 图表数据
                
        Raises:
            PredictionAPIError: 预测失败时抛出
        """
        try:
            input_data = {
                'current_traffic': params['current_traffic'],
                'prediction_hours': params.get('prediction_hours', 24),
                'restaurant_config': params.get('restaurant_config', {})
            }
            
            context = PredictionContext(**params.get('context', {}))
            result = self.traffic_predictor.predict(input_data, context)
            
            # 转换为可序列化的格式
            return {
                'time_slots': result.time_slots,
                'predicted_traffic': [int(x) for x in result.predicted_traffic],
                'confidence_intervals': [(int(l), int(u)) for l, u in result.confidence_intervals],
                'peak_periods': [
                    {
                        'start_time': p['start_time'],
                        'end_time': p['end_time'],
                        'duration_hours': int(p['duration_hours']),
                        'peak_traffic': int(p['peak_traffic']),
                        'avg_traffic': float(p['avg_traffic'])
                    }
                    for p in result.peak_periods
                ],
                'chart_data': result.chart_data
            }
            
        except Exception as e:
            raise PredictionAPIError(f"人流量预测失败: {str(e)}")
    
    def analyze_time_series(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        统一的时间序列分析接口
        
        Args:
            params: 参数字典
                - method: 分析方法 ('fit', 'predict', 'decompose')
                - data: 时间序列数据
                - steps: 预测步数 (predict方法需要)
                - order: ARIMA模型阶数 (fit方法需要)
                - period: 季节周期 (decompose方法需要)
                - confidence_level: 置信水平 (predict方法需要)
                
        Returns:
            Dict[str, Any]: 分析结果
                - fit方法: {'success': bool}
                - predict方法: {
                    'predictions': 预测值列表,
                    'confidence_intervals': 置信区间,
                    'forecast_dates': 预测日期
                  }
                - decompose方法: {
                    'trend': 趋势成分,
                    'seasonal': 季节性成分,
                    'residual': 残差成分,
                    'original': 原始数据
                  }
                
        Raises:
            PredictionAPIError: 分析失败时抛出
        """
        try:
            method = params.get('method', 'decompose')
            if method == 'fit':
                success = self.time_series_analyzer.fit_arima_model(
                    params['data'],
                    params.get('order', (1,1,1))
                )
                return {'success': bool(success)}
            elif method == 'predict':
                result = self.time_series_analyzer.predict_future_values(
                    params['steps'],
                    params.get('confidence_level', 0.95)
                )
                return {
                    'predictions': [float(x) for x in result['predictions']],
                    'confidence_intervals': [(float(l), float(u)) for l, u in result['confidence_intervals']],
                    'forecast_dates': result['forecast_dates']
                }
            elif method == 'decompose':
                result = self.time_series_analyzer.decompose_seasonal(
                    params['data'],
                    params.get('period', 24)
                )
                return {
                    'trend': [float(x) for x in result['trend']],
                    'seasonal': [float(x) for x in result['seasonal']],
                    'residual': [float(x) for x in result['residual']],
                    'original': [float(x) for x in result['original']]
                }
            else:
                raise PredictionAPIError(f"Unknown method: {method}")
                
        except Exception as e:
            raise PredictionAPIError(f"时间序列分析失败: {str(e)}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        获取预测系统状态
        
        Returns:
            Dict[str, Any]: 系统状态信息
                - is_initialized: 是否已初始化
                - last_update: 最后更新时间
                - cache_status: 缓存状态
        """
        return {
            'is_initialized': self.is_initialized,
            'last_update': self.last_training_time.isoformat() if self.last_training_time else None,
            'cache_status': {
                'cache_size': len(self.prediction_cache),
                'cache_keys': list(self.prediction_cache.keys())
            }
        }
    
    def clear_prediction_cache(self) -> bool:
        """
        清除预测缓存
        
        Returns:
            bool: 清除是否成功
        """
        try:
            self.prediction_cache.clear()
            return True
        except Exception:
            return False 