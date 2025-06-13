"""
餐厅排队预测系统 - 人流量预测器
专门用于预测餐厅人流量趋势和高峰时段
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from predictors.base_predictor import BasePredictor, InsufficientDataError, BasePredictorError
from algorithms.time_series_analysis import TimeSeriesAnalyzer
import numpy as np
from models.prediction_models import (
    QueueData, RestaurantConfig, HistoricalData, 
    PredictionContext, TrafficPrediction
)


class TrafficPredictor(BasePredictor):
    """
    人流量预测器
    
    主要功能：
    1. 预测未来24小时的人流量变化
    2. 识别人流高峰时段
    3. 生成可视化图表数据
    4. 提供经营决策支持
    """
    
    def __init__(self):
        """初始化人流量预测器"""
        super().__init__("TrafficPredictor")
        self.time_series_analyzer = TimeSeriesAnalyzer()
        self.pattern_library = {}
        self.seasonal_factors = {}
        self.prediction_history = []
        self.default_patterns = {
            'fast_food': {
                'peak_hours': [12, 13, 18, 19],
                'base_traffic': [5, 3, 2, 2, 3, 5, 8, 12, 15, 18, 25, 35, 45, 35, 20, 15, 12, 25, 40, 35, 20, 15, 10, 8],
                'weekend_multiplier': 1.3
            },
            'casual_dining': {
                'peak_hours': [12, 13, 18, 19, 20],
                'base_traffic': [2, 1, 1, 1, 2, 3, 5, 8, 12, 15, 20, 30, 40, 25, 15, 10, 8, 15, 35, 45, 30, 20, 12, 5],
                'weekend_multiplier': 1.5
            },
            'fine_dining': {
                'peak_hours': [19, 20, 21],
                'base_traffic': [0, 0, 0, 0, 0, 0, 0, 2, 3, 5, 8, 12, 15, 10, 8, 5, 3, 8, 20, 35, 25, 15, 8, 3],
                'weekend_multiplier': 1.2
            }
        }
    
    def train(self, historical_data: HistoricalData, config: RestaurantConfig) -> bool:
        """
        训练人流量预测模型
        
        Args:
            historical_data: 历史人流量数据
            config: 餐厅配置信息
            
        Returns:
            bool: 训练是否成功
            
        Raises:
            InsufficientDataError: 历史数据不足时抛出
        """
        pass
    
    def predict(self, input_data: Dict[str, Any], context: PredictionContext) -> TrafficPrediction:
        """
        预测未来人流量趋势
        
        Args:
            input_data: 包含以下字段的字典
                - current_traffic: int 当前人流量
                - prediction_hours: int 预测时长(小时)，默认24
                - restaurant_config: RestaurantConfig 餐厅配置
            context: 预测上下文信息
            
        Returns:
            TrafficPrediction: 人流量预测结果
            
        Raises:
            BasePredictorError: 预测失败时抛出
        """
        try:
            # 提取输入数据
            current_traffic = input_data.get('current_traffic', 0)
            prediction_hours = input_data.get('prediction_hours', 24)
            prediction_intervals = input_data.get('predictionIntervals', prediction_hours * 12)  # 默认5分钟间隔
            interval_minutes = input_data.get('intervalMinutes', 5)  # 默认5分钟间隔
            restaurant_config = input_data.get('restaurant_config')
            
            if not restaurant_config:
                raise BasePredictorError("缺少餐厅配置信息")
            
            # 生成时间段列表（支持分钟间隔）
            time_slots = self._generate_time_slots_minutes(context.current_time, prediction_intervals, interval_minutes)
            
            # 判断是否为冷启动
            if self._is_cold_start():
                # 使用默认模式预测，转换为等效小时数
                equivalent_hours = max(1, int(prediction_intervals * interval_minutes / 60))
                # 将当前人流传递给冷启动预测
                context.current_traffic = current_traffic
                base_prediction = self._handle_cold_start_prediction(
                    restaurant_config, context, equivalent_hours
                )
                # 如果需要更多间隔点，进行插值扩展
                predicted_traffic = self._expand_prediction_to_intervals(
                    base_prediction, prediction_intervals
                )
            else:
                # 使用历史数据和时间序列分析
                predicted_traffic = self._predict_with_patterns(
                    restaurant_config, context, prediction_intervals, interval_minutes
                )
            
            # 应用外部因素调整
            predicted_traffic = self._apply_external_factors(predicted_traffic, context)
            
            # 识别高峰时段
            peak_periods = self._identify_peak_periods(predicted_traffic, time_slots)
            
            # 计算置信区间
            confidence_intervals = self._calculate_confidence_intervals(predicted_traffic)
            
            # 生成预测结果
            prediction = TrafficPrediction(
                time_slots=time_slots,
                predicted_traffic=predicted_traffic,
                confidence_intervals=confidence_intervals,
                peak_periods=peak_periods,
                chart_data={},  # 稍后生成
                prediction_horizon=prediction_intervals * interval_minutes / 60  # 转换为小时
            )
            
            # 生成图表数据
            prediction.chart_data = self._generate_chart_data(prediction)
            
            # 记录预测历史
            self._record_prediction(prediction, context)
            
            return prediction
            
        except Exception as e:
            raise BasePredictorError(f"人流量预测失败: {str(e)}")
    
    def _predict_with_time_series(self, historical_data: List[int], prediction_hours: int) -> List[int]:
        """
        使用时间序列模型预测人流量
        
        Args:
            historical_data: 历史人流量数据
            prediction_hours: 预测小时数
            
        Returns:
            List[int]: 每小时预测人流量
        """
        pass
    
    def _predict_with_ml_model(self, features: Dict[str, Any], prediction_hours: int) -> List[int]:
        """
        使用机器学习模型预测人流量
        
        Args:
            features: 特征数据（天气、节假日、活动等）
            prediction_hours: 预测小时数
            
        Returns:
            List[int]: 每小时预测人流量
        """
        pass
    
    def _handle_cold_start_prediction(self, config: RestaurantConfig, context: PredictionContext, 
                                    prediction_hours: int) -> List[int]:
        """
        处理冷启动情况的人流量预测
        
        Args:
            config: 餐厅配置
            context: 预测上下文
            prediction_hours: 预测小时数
            
        Returns:
            List[int]: 基于默认模式的预测结果
        """
        # 获取餐厅类型的默认模式
        restaurant_type = config.restaurant_type
        default_pattern = self.default_patterns.get(restaurant_type, self.default_patterns['casual_dining'])
        
        base_traffic = default_pattern['base_traffic']
        weekend_multiplier = default_pattern['weekend_multiplier']
        
        # 生成预测结果
        predicted_traffic = []
        current_time = context.current_time
        # 从context中获取当前人流（已在predict方法中设置）
        current_traffic = getattr(context, 'current_traffic', 0)
        
        print(f"冷启动预测: 当前时间={current_time}, 当前人流={current_traffic}, 预测{prediction_hours}小时")
        
        for hour_offset in range(prediction_hours):
            target_time = current_time + timedelta(hours=hour_offset)
            hour_of_day = target_time.hour
            
            # 获取基础流量
            base_value = base_traffic[hour_of_day]
            
            # 周末调整
            if target_time.weekday() >= 5:  # 周六、周日
                base_value = int(base_value * weekend_multiplier)
            
            # 考虑当前实际人流，进行动态调整
            if hour_offset == 0:  # 第一个预测点，基于当前实际情况
                # 如果当前人流与模式差异很大，进行调整
                pattern_current = base_traffic[current_time.hour]
                if current_traffic > 0 and pattern_current > 0:
                    adjustment_ratio = current_traffic / pattern_current
                    base_value = int(base_value * adjustment_ratio * 0.7 + base_value * 0.3)  # 70%基于实际，30%基于模式
                    print(f"动态调整: 模式值={pattern_current}, 实际值={current_traffic}, 调整比例={adjustment_ratio:.2f}, 调整后={base_value}")
            
            # 添加时间趋势变化（深夜时间人流递减）
            if 22 <= hour_of_day or hour_of_day <= 6:  # 深夜到早晨
                # 深夜人流逐渐减少
                time_decay = 0.8 + 0.2 * np.random.random()  # 80%-100%的衰减
                base_value = int(base_value * time_decay)
                print(f"深夜衰减: {hour_of_day}时, 衰减系数={time_decay:.2f}, 调整后={base_value}")
            
            # 添加一些随机变化
            variation = np.random.normal(0, max(1, base_value * 0.15))  # 增加变化幅度
            final_value = max(0, int(base_value + variation))
            
            predicted_traffic.append(final_value)
            print(f"预测点{hour_offset+1}: {target_time.hour}时 -> {final_value}人")
        
        return predicted_traffic
    
    def _identify_peak_periods(self, predicted_traffic: List[int], time_slots: List[str]) -> List[Dict[str, Any]]:
        """
        识别人流高峰时段
        
        Args:
            predicted_traffic: 预测的人流量数据
            time_slots: 对应的时间段
            
        Returns:
            List[Dict[str, Any]]: 高峰时段信息列表
        """
        if not predicted_traffic or len(predicted_traffic) < 2:
            return []
        
        # 改进的高峰期检测算法
        max_traffic = max(predicted_traffic)
        avg_traffic = np.mean(predicted_traffic)
        
        # 动态阈值：考虑最大值和平均值的关系
        if max_traffic <= 5:  # 整体人流很低
            peak_threshold = max_traffic * 0.8  # 接近最大值才算高峰
        elif max_traffic > avg_traffic * 3:  # 有明显峰值
            peak_threshold = avg_traffic * 1.5  # 高于平均值50%
        else:  # 一般情况
            peak_threshold = avg_traffic * 1.3  # 高于平均值30%
        
        print(f"高峰检测: 最大值={max_traffic}, 平均值={avg_traffic:.1f}, 阈值={peak_threshold:.1f}")
        
        peak_periods = []
        in_peak = False
        peak_start = None
        
        for i, (traffic, time_slot) in enumerate(zip(predicted_traffic, time_slots)):
            if traffic >= peak_threshold and not in_peak:
                # 开始高峰期
                in_peak = True
                peak_start = i
                print(f"高峰开始: {time_slot} ({traffic}人)")
            elif traffic < peak_threshold and in_peak:
                # 结束高峰期
                in_peak = False
                peak_traffic = max(predicted_traffic[peak_start:i])
                avg_peak_traffic = np.mean(predicted_traffic[peak_start:i])
                
                peak_periods.append({
                    'start_time': time_slots[peak_start],
                    'end_time': time_slots[i-1],
                    'duration_hours': i - peak_start,
                    'peak_traffic': peak_traffic,
                    'avg_traffic': avg_peak_traffic
                })
                print(f"高峰结束: {time_slots[i-1]} (峰值={peak_traffic}人)")
        
        # 处理最后一个高峰期（如果预测结束时仍在高峰期）
        if in_peak:
            peak_traffic = max(predicted_traffic[peak_start:])
            avg_peak_traffic = np.mean(predicted_traffic[peak_start:])
            
            peak_periods.append({
                'start_time': time_slots[peak_start],
                'end_time': time_slots[-1],
                'duration_hours': len(time_slots) - peak_start,
                'peak_traffic': peak_traffic,
                'avg_traffic': avg_peak_traffic
            })
            print(f"高峰持续到结束: {time_slots[-1]} (峰值={peak_traffic}人)")
        
        # 如果没有检测到高峰期，但有明显的最高点，标记最高点为高峰
        if not peak_periods and max_traffic > avg_traffic * 1.2:
            max_index = predicted_traffic.index(max_traffic)
            peak_periods.append({
                'start_time': time_slots[max_index],
                'end_time': time_slots[max_index],
                'duration_hours': 1,
                'peak_traffic': max_traffic,
                'avg_traffic': max_traffic
            })
            print(f"单点高峰: {time_slots[max_index]} ({max_traffic}人)")
        
        return peak_periods
    
    def _calculate_confidence_intervals(self, predictions: List[int]) -> List[tuple]:
        """
        计算预测结果的置信区间
        
        Args:
            predictions: 预测结果
            
        Returns:
            List[tuple]: 每个预测点的置信区间 (下界, 上界)
        """
        confidence_intervals = []
        
        for pred in predictions:
            # 简化的置信区间计算：基于预测值的百分比
            error_margin = pred * 0.2  # 20%的误差范围
            lower_bound = max(0, int(pred - error_margin))
            upper_bound = int(pred + error_margin)
            confidence_intervals.append((lower_bound, upper_bound))
        
        return confidence_intervals
    
    def _generate_chart_data(self, prediction: TrafficPrediction) -> Dict[str, Any]:
        """
        生成图表数据
        
        Args:
            prediction: 人流量预测结果
            
        Returns:
            Dict[str, Any]: 图表数据字典
        """
        chart_data = {
            'type': 'line_chart',
            'title': '人流量预测趋势',
            'x_axis': {
                'label': '时间',
                'data': prediction.time_slots
            },
            'y_axis': {
                'label': '人流量',
                'data': prediction.predicted_traffic
            },
            'confidence_bands': {
                'lower': [ci[0] for ci in prediction.confidence_intervals],
                'upper': [ci[1] for ci in prediction.confidence_intervals]
            },
            'peak_markers': [
                {
                    'start': period['start_time'],
                    'end': period['end_time'],
                    'label': f"高峰期 (峰值: {period['peak_traffic']})"
                }
                for period in prediction.peak_periods
            ],
            'statistics': {
                'max_traffic': max(prediction.predicted_traffic),
                'min_traffic': min(prediction.predicted_traffic),
                'avg_traffic': np.mean(prediction.predicted_traffic),
                'total_peaks': len(prediction.peak_periods)
            }
        }
        
        return chart_data
    
    def _apply_external_factors(self, base_prediction: List[int], context: PredictionContext) -> List[int]:
        """
        应用外部因素调整预测结果
        
        Args:
            base_prediction: 基础预测结果
            context: 预测上下文（天气、节假日等）
            
        Returns:
            List[int]: 调整后的预测结果
        """
        pass
    
    def _extract_time_features(self, current_time: datetime, prediction_hours: int) -> Dict[str, Any]:
        """
        提取时间特征
        
        Args:
            current_time: 当前时间
            prediction_hours: 预测时长
            
        Returns:
            Dict[str, Any]: 时间特征字典
        """
        pass
    
    def get_business_insights(self, prediction: TrafficPrediction) -> Dict[str, Any]:
        """
        基于预测结果生成经营洞察
        
        Args:
            prediction: 人流量预测结果
            
        Returns:
            Dict[str, Any]: 经营建议和洞察
        """
        insights = {
            'staffing_recommendations': [],
            'inventory_suggestions': [],
            'operational_tips': [],
            'revenue_opportunities': []
        }
        
        # 分析高峰期
        if prediction.peak_periods:
            for period in prediction.peak_periods:
                insights['staffing_recommendations'].append(
                    f"在 {period['start_time']} - {period['end_time']} 期间增加服务人员，预计峰值人流 {period['peak_traffic']} 人"
                )
                
                insights['inventory_suggestions'].append(
                    f"为 {period['start_time']} 的高峰期准备充足库存"
                )
        
        # 分析整体趋势
        avg_traffic = np.mean(prediction.predicted_traffic)
        max_traffic = max(prediction.predicted_traffic)
        
        if max_traffic > avg_traffic * 2:
            insights['operational_tips'].append("存在明显的人流高峰，建议实施错峰优惠策略")
        
        if len(prediction.peak_periods) > 3:
            insights['operational_tips'].append("多个高峰时段，建议优化服务流程以提高效率")
        
        # 收入机会分析
        total_predicted = sum(prediction.predicted_traffic)
        insights['revenue_opportunities'].append(
            f"预测期内总客流量约 {total_predicted} 人次，建议制定相应的营销策略"
        )
        
        return insights
    
    def _is_cold_start(self) -> bool:
        """判断是否为冷启动状态"""
        return len(self.prediction_history) < 5
    
    def _generate_time_slots(self, start_time: datetime, hours: int) -> List[str]:
        """生成时间段列表（小时间隔）"""
        time_slots = []
        for i in range(hours):
            slot_time = start_time + timedelta(hours=i)
            time_slots.append(slot_time.strftime("%Y-%m-%d %H:00"))
        return time_slots
    
    def _generate_time_slots_minutes(self, start_time: datetime, intervals: int, interval_minutes: int) -> List[str]:
        """生成时间段列表（分钟间隔），从下一个5分钟时刻开始"""
        time_slots = []
        
        # 计算下一个5分钟时刻
        current_minute = start_time.minute
        next_5min_minute = ((current_minute // 5) + 1) * 5
        
        if next_5min_minute >= 60:
            # 如果超过60分钟，进入下一小时
            next_start_time = start_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        else:
            next_start_time = start_time.replace(minute=next_5min_minute, second=0, microsecond=0)
        
        print(f"预测起始时间调整: {start_time.strftime('%H:%M')} -> {next_start_time.strftime('%H:%M')} (下一个5分钟时刻)")
        
        for i in range(intervals):
            slot_time = next_start_time + timedelta(minutes=i * interval_minutes)
            time_slots.append(slot_time.strftime("%H:%M"))
        
        return time_slots
    
    def _expand_prediction_to_intervals(self, base_prediction: List[int], target_intervals: int) -> List[int]:
        """将基础预测扩展到目标间隔数，并添加分钟级变化"""
        if len(base_prediction) >= target_intervals:
            return base_prediction[:target_intervals]
        
        # 线性插值扩展
        extended_prediction = []
        print(f"扩展预测: 基础{len(base_prediction)}点 -> 目标{target_intervals}点")
        
        for i in range(target_intervals):
            # 计算在原始预测中的位置
            pos = i * len(base_prediction) / target_intervals
            idx = int(pos)
            if idx >= len(base_prediction) - 1:
                base_value = base_prediction[-1]
            else:
                # 线性插值
                frac = pos - idx
                base_value = base_prediction[idx] * (1 - frac) + base_prediction[idx + 1] * frac
            
            # 添加分钟级的微小变化
            minute_variation = np.random.normal(0, max(0.5, base_value * 0.1))
            final_value = max(0, int(base_value + minute_variation))
            
            extended_prediction.append(final_value)
            print(f"扩展点{i+1}: 基础值={base_value:.1f}, 变化={minute_variation:.1f}, 最终={final_value}")
        
        return extended_prediction
    
    def _predict_with_patterns(self, config: RestaurantConfig, context: PredictionContext, 
                             prediction_intervals: int, interval_minutes: int) -> List[int]:
        """使用历史模式预测（简化版本）"""
        # 如果有历史数据，这里可以使用时间序列分析
        # 目前使用默认模式作为基础，转换为等效小时数
        equivalent_hours = max(1, prediction_intervals * interval_minutes // 60)
        base_prediction = self._handle_cold_start_prediction(config, context, equivalent_hours)
        
        # 如果需要更多间隔点，进行插值
        if len(base_prediction) < prediction_intervals:
            # 简单线性插值扩展到所需间隔数
            extended_prediction = []
            for i in range(prediction_intervals):
                # 计算在原始预测中的位置
                pos = i * len(base_prediction) / prediction_intervals
                idx = int(pos)
                if idx >= len(base_prediction) - 1:
                    extended_prediction.append(base_prediction[-1])
                else:
                    # 线性插值
                    frac = pos - idx
                    value = base_prediction[idx] * (1 - frac) + base_prediction[idx + 1] * frac
                    extended_prediction.append(int(value))
            return extended_prediction
        else:
            return base_prediction[:prediction_intervals]
    
    def _apply_external_factors(self, base_prediction: List[int], context: PredictionContext) -> List[int]:
        """
        应用外部因素调整预测结果
        
        Args:
            base_prediction: 基础预测结果
            context: 预测上下文（天气、节假日等）
            
        Returns:
            List[int]: 调整后的预测结果
        """
        adjusted_prediction = base_prediction.copy()
        
        # 节假日调整
        if context.is_holiday:
            adjusted_prediction = [int(x * 1.2) for x in adjusted_prediction]  # 节假日增加20%
        
        # 天气调整
        if context.weather_info:
            weather_condition = context.weather_info.get('condition', 'sunny')
            if weather_condition in ['rainy', 'stormy']:
                adjusted_prediction = [int(x * 0.8) for x in adjusted_prediction]  # 恶劣天气减少20%
            elif weather_condition == 'sunny':
                adjusted_prediction = [int(x * 1.1) for x in adjusted_prediction]  # 好天气增加10%
        
        # 特殊活动调整
        if context.local_events:
            adjusted_prediction = [int(x * 1.3) for x in adjusted_prediction]  # 有活动增加30%
        
        return adjusted_prediction
    
    def _record_prediction(self, prediction: TrafficPrediction, context: PredictionContext) -> None:
        """记录预测历史"""
        self.prediction_history.append({
            'prediction': prediction,
            'context': context,
            'timestamp': datetime.now()
        })
        
        # 保持历史记录在合理范围内
        if len(self.prediction_history) > 100:
            self.prediction_history = self.prediction_history[-50:] 