"""
餐厅排队预测系统 - 等待时间预测器
专门用于预测顾客的排队等待时间
"""

from typing import Dict, Any, Optional
from datetime import datetime
from predictors.base_predictor import BasePredictor, InsufficientDataError, BasePredictorError
from algorithms.queue_theory import QueueTheoryCalculator
from models.prediction_models import (
    QueueData, RestaurantConfig, HistoricalData, 
    PredictionContext, WaitTimePrediction
)


class WaitTimePredictor(BasePredictor):
    """
    等待时间预测器
    
    主要功能：
    1. 基于排队论模型预测顾客等待时间
    2. 结合历史模式进行预测调整
    3. 处理冷启动问题
    """
    
    def __init__(self):
        """初始化等待时间预测器"""
        super().__init__("WaitTimePredictor")
        self.queue_calculator = QueueTheoryCalculator()
        self.pattern_adjustments = {}
        self.prediction_history = []
        self.default_service_times = {
            'fast_food': 8.0,
            'casual_dining': 45.0,
            'fine_dining': 90.0
        }
        self.default_service_rates = {
            'fast_food': 7.5,  # 顾客/小时
            'casual_dining': 1.3,
            'fine_dining': 0.7
        }
    
    def train(self, historical_data: HistoricalData, config: RestaurantConfig) -> bool:
        """
        训练等待时间预测模型
        
        Args:
            historical_data: 历史排队和服务数据
            config: 餐厅配置信息
            
        Returns:
            bool: 训练是否成功
            
        Raises:
            InsufficientDataError: 历史数据不足时抛出
        """
        pass
    
    def predict(self, input_data: Dict[str, Any], context: PredictionContext) -> WaitTimePrediction:
        """
        预测顾客等待时间
        
        Args:
            input_data: 包含以下字段的字典
                - queue_data: QueueData 当前排队状态
                - customer_position: int 顾客在队列中的位置
                - restaurant_config: RestaurantConfig 餐厅配置
            context: 预测上下文信息
            
        Returns:
            WaitTimePrediction: 等待时间预测结果
            
        Raises:
            BasePredictorError: 预测失败时抛出
        """
        try:
            # 提取输入数据
            queue_data = input_data.get('queue_data')
            customer_position = input_data.get('customer_position', queue_data.current_queue_length + 1)
            restaurant_config = input_data.get('restaurant_config')
            
            if not queue_data or not restaurant_config:
                raise BasePredictorError("缺少必要的输入数据")
            
            # 1. 计算基础等待时间
            base_wait_time = self._calculate_queue_theory_wait_time(queue_data, customer_position)
            
            # 2. 应用历史模式调整
            adjusted_wait_time = self._apply_pattern_adjustment(base_wait_time, context)
            
            # 3. 处理冷启动情况
            if self._is_cold_start(context):
                adjusted_wait_time = self._handle_cold_start(restaurant_config, queue_data)
            
            # 4. 计算置信度
            confidence = self._calculate_confidence_level({
                'data_availability': len(self.prediction_history),
                'queue_stability': self._assess_queue_stability(queue_data),
                'time_of_day': context.current_time.hour if context.current_time else 12
            })
            
            # 5. 生成预测范围
            min_time, max_time = self._generate_prediction_range(adjusted_wait_time, confidence)
            
            # 6. 创建预测结果
            message = self._generate_customer_message_simple(adjusted_wait_time)
            
            prediction = WaitTimePrediction(
                customer_position=customer_position,
                estimated_wait_time=max(0, adjusted_wait_time),
                confidence_level=confidence,
                prediction_range=(min_time, max_time),
                message=message,
                timestamp=context.current_time or datetime.now()
            )
            
            # 7. 记录预测历史
            self._record_prediction(prediction, queue_data, context)
            
            return prediction
            
        except Exception as e:
            raise BasePredictorError(f"等待时间预测失败: {str(e)}")
    
    def _calculate_queue_theory_wait_time(self, queue_data: QueueData, customer_position: int) -> float:
        """
        使用排队论计算基础等待时间
        
        Args:
            queue_data: 当前排队数据
            customer_position: 顾客位置
            
        Returns:
            float: 基础等待时间(分钟)
        """
        try:
            # 从平均服务时间计算服务率
            avg_service_time = queue_data.average_service_time or 15.0  # 默认15分钟
            service_rate = 60 / avg_service_time  # 转换为每小时服务率
            
            # 使用排队论计算器
            wait_time = self.queue_calculator.calculate_customer_position_wait_time(
                current_queue_length=queue_data.current_queue_length,
                customer_position=customer_position,
                service_rate=service_rate,
                servers=queue_data.active_servers or 1
            )
            return wait_time
            
        except Exception as e:
            # 如果排队论计算失败，使用简单估算
            avg_service_time = queue_data.average_service_time or 15.0
            servers = queue_data.active_servers or 1
            people_ahead = max(0, customer_position - 1)
            
            # 简单计算：前面的人数 / 服务台数量 * 平均服务时间
            estimated_wait = (people_ahead / servers) * avg_service_time
            return estimated_wait
    
    def _apply_pattern_adjustment(self, base_wait_time: float, context: PredictionContext) -> float:
        """
        根据历史模式调整等待时间预测
        
        Args:
            base_wait_time: 基础等待时间
            context: 预测上下文
            
        Returns:
            float: 调整后的等待时间
        """
        if not context.current_time:
            return base_wait_time
        
        # 获取当前时间信息
        hour = context.current_time.hour
        day_of_week = context.current_time.weekday()  # 0=Monday, 6=Sunday
        
        # 时段调整因子
        time_adjustment = 1.0
        
        # 高峰时段调整 (11-13点, 18-20点)
        if (11 <= hour <= 13) or (18 <= hour <= 20):
            time_adjustment = 1.3  # 高峰时段增加30%
        # 低谷时段调整 (14-17点, 21-23点)
        elif (14 <= hour <= 17) or (21 <= hour <= 23):
            time_adjustment = 0.8  # 低谷时段减少20%
        # 深夜时段 (0-6点)
        elif 0 <= hour <= 6:
            time_adjustment = 0.6  # 深夜时段减少40%
        
        # 周末调整
        weekend_adjustment = 1.0
        if day_of_week >= 5:  # 周六、周日
            weekend_adjustment = 1.2  # 周末增加20%
        
        # 应用调整
        adjusted_time = base_wait_time * time_adjustment * weekend_adjustment
        
        return adjusted_time
    
    def _handle_cold_start(self, restaurant_config: RestaurantConfig, queue_data: QueueData) -> float:
        """
        处理冷启动情况的等待时间预测
        
        Args:
            restaurant_config: 餐厅配置
            queue_data: 当前排队数据
            
        Returns:
            float: 冷启动预测的等待时间
        """
        # 根据餐厅类型获取默认服务时间
        restaurant_type = getattr(restaurant_config, 'restaurant_type', 'casual_dining')
        default_service_time = self.default_service_times.get(restaurant_type, 15.0)
        
        # 获取服务台数量
        servers = queue_data.active_servers or getattr(restaurant_config, 'total_servers', 1)
        
        # 计算队列中的位置
        queue_length = queue_data.current_queue_length
        
        # 冷启动简单估算：队列长度 / 服务台数量 * 平均服务时间
        estimated_wait = (queue_length / servers) * default_service_time
        
        # 添加一些不确定性缓冲 (增加20%)
        estimated_wait *= 1.2
        
        return estimated_wait
    
    def _calculate_confidence_level(self, prediction_context: Dict[str, Any]) -> float:
        """
        计算等待时间预测的置信度
        
        Args:
            prediction_context: 预测上下文信息
            
        Returns:
            float: 置信度 (0-1)
        """
        pass
    
    def _generate_prediction_range(self, estimated_time: float, confidence: float) -> tuple:
        """
        生成预测时间范围
        
        Args:
            estimated_time: 预测的等待时间
            confidence: 预测置信度
            
        Returns:
            tuple: (最小时间, 最大时间)
        """
        pass
    
    def _generate_customer_message(self, prediction: WaitTimePrediction) -> str:
        """
        生成给顾客的友好提示信息
        
        Args:
            prediction: 等待时间预测结果
            
        Returns:
            str: 给顾客的提示信息
        """
        pass
    
    def update_real_time_data(self, actual_wait_time: float, predicted_wait_time: float) -> None:
        """
        使用实际等待时间更新模型
        
        Args:
            actual_wait_time: 实际等待时间
            predicted_wait_time: 之前的预测时间
        """
        # 记录预测误差
        error = abs(actual_wait_time - predicted_wait_time)
        accuracy = max(0, 1 - error / max(actual_wait_time, 1))
        
        # 更新预测历史
        self.prediction_history.append({
            'actual': actual_wait_time,
            'predicted': predicted_wait_time,
            'error': error,
            'accuracy': accuracy,
            'timestamp': datetime.now()
        })
        
        # 保持历史记录在合理范围内
        if len(self.prediction_history) > 1000:
            self.prediction_history = self.prediction_history[-500:]
    
    def _is_cold_start(self, context: PredictionContext) -> bool:
        """判断是否为冷启动状态 - 修改判断条件"""
        # 如果有足够的历史数据，就不是冷启动
        return len(self.prediction_history) < 3  # 降低冷启动阈值
    
    def _assess_queue_stability(self, queue_data: QueueData) -> float:
        """评估队列稳定性"""
        # 简化的稳定性评估，基于队列长度和服务台数量
        servers = queue_data.active_servers or 1
        queue_length = queue_data.current_queue_length
        
        # 计算每个服务台的平均队列长度
        avg_queue_per_server = queue_length / servers
        
        # 根据平均队列长度评估稳定性
        if avg_queue_per_server <= 2:
            return 0.9  # 很稳定
        elif avg_queue_per_server <= 5:
            return 0.7  # 中等稳定
        elif avg_queue_per_server <= 10:
            return 0.5  # 不太稳定
        else:
            return 0.3  # 很不稳定
    
    def _record_prediction(self, prediction: WaitTimePrediction, queue_data: QueueData, context: PredictionContext) -> None:
        """记录预测结果"""
        # 这里可以记录预测日志，用于后续分析和改进
        pass
    
    def _calculate_confidence_level(self, prediction_context: Dict[str, Any]) -> float:
        """
        计算等待时间预测的置信度
        
        Args:
            prediction_context: 预测上下文信息
            
        Returns:
            float: 置信度 (0-1)
        """
        base_confidence = 0.7  # 基础置信度
        
        # 数据可用性调整
        data_points = prediction_context.get('data_availability', 0)
        if data_points > 50:
            data_adjustment = 0.2
        elif data_points > 20:
            data_adjustment = 0.1
        elif data_points > 5:
            data_adjustment = 0.05
        else:
            data_adjustment = -0.1  # 数据不足降低置信度
        
        # 队列稳定性调整
        stability = prediction_context.get('queue_stability', 0.6)
        stability_adjustment = (stability - 0.6) * 0.2
        
        # 时间因子调整 (工作时间置信度更高)
        hour = prediction_context.get('time_of_day', 12)
        if 9 <= hour <= 21:
            time_adjustment = 0.1
        else:
            time_adjustment = -0.05
        
        # 计算最终置信度
        confidence = base_confidence + data_adjustment + stability_adjustment + time_adjustment
        
        return max(0.1, min(0.95, confidence))  # 限制在0.1-0.95之间
    
    def _generate_prediction_range(self, estimated_time: float, confidence: float) -> tuple:
        """
        生成预测时间范围
        
        Args:
            estimated_time: 预测的等待时间
            confidence: 预测置信度
            
        Returns:
            tuple: (最小时间, 最大时间)
        """
        # 根据置信度计算误差范围
        error_margin = estimated_time * (1 - confidence) * 0.5
        
        min_time = max(0, estimated_time - error_margin)
        max_time = estimated_time + error_margin
        
        return (min_time, max_time)
    
    def _generate_customer_message(self, prediction: WaitTimePrediction) -> str:
        """
        生成给顾客的友好提示信息
        
        Args:
            prediction: 等待时间预测结果
            
        Returns:
            str: 给顾客的提示信息
        """
        wait_time = prediction.estimated_wait_time
        confidence = prediction.confidence_level
        
        if wait_time < 5:
            return "您很快就能得到服务，预计等待时间不超过5分钟。"
        elif wait_time < 15:
            return f"预计等待时间约{int(wait_time)}分钟，请稍候。"
        elif wait_time < 30:
            return f"当前排队人数较多，预计需要等待{int(wait_time)}分钟左右。"
        else:
            return f"当前排队时间较长，预计需要等待{int(wait_time)}分钟以上，建议您考虑其他时间再来。"
    
    def _generate_customer_message_simple(self, wait_time: float) -> str:
        """生成简化的顾客消息"""
        if wait_time < 5:
            return "很快就能得到服务"
        elif wait_time < 15:
            return f"预计等待约{int(wait_time)}分钟"
        elif wait_time < 30:
            return f"需要等待约{int(wait_time)}分钟"
        else:
            return f"等待时间较长，约{int(wait_time)}分钟"

    def add_historical_data(self, historical_data: Dict[str, Any]) -> None:
        """
        添加历史数据到预测器中，避免冷启动
        
        Args:
            historical_data: 包含历史数据的字典
        """
        try:
            # 从历史数据中提取有用信息
            recent_person_counts = historical_data.get('recentPersonCounts', [])
            avg_person_count = historical_data.get('averagePersonCount', 0)
            person_count_variance = historical_data.get('personCountVariance', 0)
            
            # 基于历史数据创建模拟的预测历史记录
            if recent_person_counts:
                for i, person_count in enumerate(recent_person_counts):
                    # 创建模拟的预测记录
                    simulated_prediction = {
                        'actual': person_count * 5,  # 假设每人平均等待5分钟
                        'predicted': person_count * 5,  # 初始假设预测准确
                        'error': 0,
                        'accuracy': 1.0,
                        'timestamp': datetime.now()
                    }
                    self.prediction_history.append(simulated_prediction)
            
            # 如果没有具体的人数记录，至少添加一些基础记录避免冷启动
            if not self.prediction_history and avg_person_count > 0:
                for i in range(5):  # 添加5条模拟记录
                    simulated_prediction = {
                        'actual': avg_person_count * 5,
                        'predicted': avg_person_count * 5,
                        'error': person_count_variance,
                        'accuracy': max(0.5, 1.0 - person_count_variance / 100),
                        'timestamp': datetime.now()
                    }
                    self.prediction_history.append(simulated_prediction)
            
            print(f"添加了历史数据，预测历史记录数量: {len(self.prediction_history)}")
            
        except Exception as e:
            print(f"添加历史数据失败: {e}") 