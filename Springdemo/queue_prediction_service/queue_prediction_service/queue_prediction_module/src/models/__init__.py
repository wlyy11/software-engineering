"""
数据模型模块
"""

from .prediction_models import (
    QueueData,
    RestaurantConfig, 
    WaitTimePrediction,
    TrafficPrediction,
    HistoricalData,
    PredictionContext
)

__all__ = [
    'QueueData',
    'RestaurantConfig',
    'WaitTimePrediction', 
    'TrafficPrediction',
    'HistoricalData',
    'PredictionContext'
] 