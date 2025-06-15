"""
餐厅排队预测系统 - 预测器基类
定义所有预测器的通用接口和基础功能
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from models.prediction_models import (
    QueueData, RestaurantConfig, HistoricalData, 
    PredictionContext, WaitTimePrediction, TrafficPrediction
)


class BasePredictorError(Exception):
    """预测器基础异常类"""
    pass


class InsufficientDataError(BasePredictorError):
    """数据不足异常"""
    pass


class BasePredictor(ABC):
    """
    预测器基类
    
    所有具体预测器都应继承此类并实现抽象方法
    """
    
    def __init__(self, name: str):
        """
        初始化预测器
        
        Args:
            name: 预测器名称
        """
        self.name = name
        self.is_trained = False
        self.confidence_threshold = 0.5
        self.last_update_time = None
    
    @abstractmethod
    def train(self, historical_data: HistoricalData, config: RestaurantConfig) -> bool:
        """
        训练预测模型
        
        Args:
            historical_data: 历史数据
            config: 餐厅配置信息
            
        Returns:
            bool: 训练是否成功
            
        Raises:
            InsufficientDataError: 当历史数据不足时抛出
        """
        pass
    
    @abstractmethod
    def predict(self, input_data: Dict[str, Any], context: PredictionContext) -> Dict[str, Any]:
        """
        执行预测
        
        Args:
            input_data: 输入数据
            context: 预测上下文信息
            
        Returns:
            Dict[str, Any]: 预测结果
            
        Raises:
            BasePredictorError: 预测过程中的异常
        """
        pass
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        验证输入数据的有效性
        
        Args:
            input_data: 待验证的输入数据
            
        Returns:
            bool: 数据是否有效
        """
        if not input_data:
            return False
        return True
    
    def calculate_confidence(self, prediction_result: Dict[str, Any]) -> float:
        """
        计算预测结果的置信度
        
        Args:
            prediction_result: 预测结果
            
        Returns:
            float: 置信度 (0-1)
        """
        # 基础置信度计算逻辑，子类可以重写
        base_confidence = 0.7 if self.is_trained else 0.3
        return base_confidence
    
    def update_model(self, new_data: Dict[str, Any]) -> bool:
        """
        使用新数据更新模型
        
        Args:
            new_data: 新的数据
            
        Returns:
            bool: 更新是否成功
        """
        # 默认实现，子类可以重写
        return True
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        获取模型信息
        
        Returns:
            Dict[str, Any]: 模型信息字典
        """
        return {
            "name": self.name,
            "is_trained": self.is_trained,
            "confidence_threshold": self.confidence_threshold,
            "last_update_time": self.last_update_time
        } 