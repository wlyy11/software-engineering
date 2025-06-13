"""
餐厅排队预测系统 - 数据模型定义
定义系统中使用的各种数据结构和模型类
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta


@dataclass
class QueueData:
    """
    当前排队数据模型
    
    Attributes:
        current_queue_length: 当前排队人数
        average_service_time: 平均服务时间(分钟)
        active_servers: 当前活跃服务台数量
        timestamp: 数据时间戳
    """
    current_queue_length: int
    average_service_time: float
    active_servers: int
    timestamp: datetime


@dataclass
class RestaurantConfig:
    """
    餐厅配置信息模型
    
    Attributes:
        restaurant_type: 餐厅类型 ('fast_food', 'casual_dining', 'fine_dining')
        max_capacity: 最大容纳人数
        table_count: 桌位数量
        operating_hours: 营业时间 (开始时间, 结束时间)
        peak_hours: 高峰时段列表
    """
    restaurant_type: str
    max_capacity: int
    table_count: int
    operating_hours: Tuple[int, int]  # (开始小时, 结束小时)
    peak_hours: List[int]


@dataclass
class WaitTimePrediction:
    """
    等待时间预测结果模型
    
    Attributes:
        customer_position: 顾客在队列中的位置
        estimated_wait_time: 预计等待时间(分钟)
        confidence_level: 预测置信度 (0-1)
        prediction_range: 预测时间范围 (最小值, 最大值)
        message: 给顾客的提示信息
        timestamp: 预测时间戳
    """
    customer_position: int
    estimated_wait_time: float
    confidence_level: float
    prediction_range: Tuple[float, float]
    message: str
    timestamp: datetime


@dataclass
class TrafficPrediction:
    """
    人流量预测结果模型
    
    Attributes:
        time_slots: 时间段列表
        predicted_traffic: 对应时间段的预测人流量
        confidence_intervals: 置信区间列表
        peak_periods: 高峰时段信息
        chart_data: 图表数据字典
        prediction_horizon: 预测时长(小时)
    """
    time_slots: List[str]
    predicted_traffic: List[int]
    confidence_intervals: List[Tuple[int, int]]
    peak_periods: List[Dict[str, any]]
    chart_data: Dict[str, any]
    prediction_horizon: int


@dataclass
class HistoricalData:
    """
    历史数据模型
    
    Attributes:
        hourly_traffic: 按小时统计的历史客流量
        daily_patterns: 每日客流模式
        weekly_patterns: 每周客流模式
        seasonal_factors: 季节性因子
        external_factors: 外部影响因素数据
    """
    hourly_traffic: Dict[str, List[int]]  # {'2024-01-01': [10, 15, 20, ...]}
    daily_patterns: Dict[str, List[int]]   # {'monday': [5, 8, 12, ...]}
    weekly_patterns: List[float]
    seasonal_factors: Dict[str, float]
    external_factors: Dict[str, any]


@dataclass
class PredictionContext:
    """
    预测上下文信息模型
    
    Attributes:
        current_time: 当前时间
        weather_info: 天气信息
        is_holiday: 是否节假日
        local_events: 周边活动信息
        special_conditions: 特殊情况标记
    """
    current_time: datetime
    weather_info: Optional[Dict[str, any]]
    is_holiday: bool
    local_events: List[str]
    special_conditions: List[str] 