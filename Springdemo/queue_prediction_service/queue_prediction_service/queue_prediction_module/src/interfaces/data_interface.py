"""
餐厅排队预测系统 - 数据接口模块
定义与外部数据源的接口规范，供其他系统连接使用
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from ..models.prediction_models import QueueData, HistoricalData, RestaurantConfig


class DataInterfaceError(Exception):
    """数据接口异常"""
    pass


class DatabaseInterface(ABC):
    """
    数据库接口抽象类
    
    定义与预约系统数据库的连接接口
    其他团队需要实现这个接口来提供数据
    """
    
    @abstractmethod
    def get_current_queue_data(self) -> QueueData:
        """
        获取当前排队数据
        
        Returns:
            QueueData: 当前排队状态数据
            
        Raises:
            DataInterfaceError: 数据获取失败时抛出
        """
        pass
    
    @abstractmethod
    def get_historical_traffic_data(self, start_date: datetime, end_date: datetime) -> HistoricalData:
        """
        获取历史人流量数据
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            HistoricalData: 历史数据
            
        Raises:
            DataInterfaceError: 数据获取失败时抛出
        """
        pass
    
    @abstractmethod
    def get_restaurant_config(self) -> RestaurantConfig:
        """
        获取餐厅配置信息
        
        Returns:
            RestaurantConfig: 餐厅配置
            
        Raises:
            DataInterfaceError: 配置获取失败时抛出
        """
        pass
    
    @abstractmethod
    def save_prediction_result(self, prediction_data: Dict[str, Any]) -> bool:
        """
        保存预测结果
        
        Args:
            prediction_data: 预测结果数据
            
        Returns:
            bool: 保存是否成功
            
        Raises:
            DataInterfaceError: 保存失败时抛出
        """
        pass
    
    @abstractmethod
    def get_real_time_updates(self) -> List[Dict[str, Any]]:
        """
        获取实时数据更新
        
        Returns:
            List[Dict[str, Any]]: 实时更新数据列表
            
        Raises:
            DataInterfaceError: 获取失败时抛出
        """
        pass


class ExternalDataInterface(ABC):
    """
    外部数据接口抽象类
    
    定义获取外部数据的接口（天气、节假日等）
    """
    
    @abstractmethod
    def get_weather_data(self, date: datetime) -> Dict[str, Any]:
        """
        获取天气数据
        
        Args:
            date: 查询日期
            
        Returns:
            Dict[str, Any]: 天气信息
                - temperature: 温度
                - weather_type: 天气类型
                - precipitation: 降水量
                - wind_speed: 风速
        """
        pass
    
    @abstractmethod
    def get_holiday_info(self, date: datetime) -> Dict[str, Any]:
        """
        获取节假日信息
        
        Args:
            date: 查询日期
            
        Returns:
            Dict[str, Any]: 节假日信息
                - is_holiday: 是否节假日
                - holiday_name: 节假日名称
                - holiday_type: 节假日类型
        """
        pass
    
    @abstractmethod
    def get_local_events(self, date: datetime, radius_km: float = 5.0) -> List[Dict[str, Any]]:
        """
        获取周边活动信息
        
        Args:
            date: 查询日期
            radius_km: 搜索半径(公里)
            
        Returns:
            List[Dict[str, Any]]: 活动信息列表
                - event_name: 活动名称
                - event_type: 活动类型
                - expected_attendance: 预期参与人数
                - distance: 距离餐厅的距离
        """
        pass


class DataAdapter:
    """
    数据适配器
    
    将外部数据转换为预测系统所需的格式
    """
    
    def __init__(self, db_interface: DatabaseInterface, 
                 external_interface: Optional[ExternalDataInterface] = None):
        """
        初始化数据适配器
        
        Args:
            db_interface: 数据库接口实现
            external_interface: 外部数据接口实现
        """
        self.db_interface = db_interface
        self.external_interface = external_interface
        self.cache = {}
        self.cache_duration = timedelta(minutes=5)
    
    def get_prediction_input_data(self, customer_position: Optional[int] = None) -> Dict[str, Any]:
        """
        获取预测所需的输入数据
        
        Args:
            customer_position: 顾客位置（等待时间预测时需要）
            
        Returns:
            Dict[str, Any]: 预测输入数据
                - queue_data: 当前排队数据
                - restaurant_config: 餐厅配置
                - historical_data: 历史数据
                - context: 预测上下文
        """
        pass
    
    def format_queue_data(self, raw_data: Dict[str, Any]) -> QueueData:
        """
        格式化排队数据
        
        Args:
            raw_data: 原始排队数据
            
        Returns:
            QueueData: 格式化后的排队数据
        """
        pass
    
    def format_historical_data(self, raw_data: List[Dict[str, Any]]) -> HistoricalData:
        """
        格式化历史数据
        
        Args:
            raw_data: 原始历史数据
            
        Returns:
            HistoricalData: 格式化后的历史数据
        """
        pass
    
    def create_prediction_context(self, current_time: datetime) -> Dict[str, Any]:
        """
        创建预测上下文
        
        Args:
            current_time: 当前时间
            
        Returns:
            Dict[str, Any]: 预测上下文信息
        """
        pass
    
    def validate_data_quality(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证数据质量
        
        Args:
            data: 待验证的数据
            
        Returns:
            Dict[str, Any]: 数据质量报告
                - is_valid: 数据是否有效
                - missing_fields: 缺失字段
                - data_issues: 数据问题
                - suggestions: 改进建议
        """
        pass
    
    def cache_data(self, key: str, data: Any, duration: Optional[timedelta] = None) -> None:
        """
        缓存数据
        
        Args:
            key: 缓存键
            data: 要缓存的数据
            duration: 缓存持续时间
        """
        pass
    
    def get_cached_data(self, key: str) -> Optional[Any]:
        """
        获取缓存数据
        
        Args:
            key: 缓存键
            
        Returns:
            Optional[Any]: 缓存的数据，如果不存在或过期则返回None
        """
        pass
    
    def clear_cache(self) -> None:
        """清除所有缓存数据"""
        pass 