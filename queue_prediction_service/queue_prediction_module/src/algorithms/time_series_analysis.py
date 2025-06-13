"""
餐厅排队预测系统 - 时间序列分析算法模块
实现ARIMA、季节性分解等时间序列预测方法
"""

from typing import List, Dict, Any, Tuple, Optional
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


class TimeSeriesError(Exception):
    """时间序列分析异常"""
    pass


class TimeSeriesAnalyzer:
    """
    时间序列分析器
    
    实现功能：
    1. ARIMA模型预测
    2. 季节性分解
    3. 趋势分析
    4. 周期性检测
    """
    
    def __init__(self):
        """初始化时间序列分析器"""
        self.model = None
        self.seasonal_components = {}
        self.trend_components = {}
        self.residual_components = {}
        self.fitted_values = []
    
    def fit_arima_model(self, data: List[float], order: Tuple[int, int, int] = (1, 1, 1)) -> bool:
        """
        拟合ARIMA模型
        
        Args:
            data: 时间序列数据
            order: ARIMA模型参数 (p, d, q)
                - p: 自回归项数
                - d: 差分次数  
                - q: 移动平均项数
                
        Returns:
            bool: 拟合是否成功
            
        Raises:
            TimeSeriesError: 拟合失败时抛出
        """
        if len(data) < 10:
            raise TimeSeriesError("数据点太少，无法拟合ARIMA模型")
        
        try:
            # 转换为numpy数组
            ts_data = np.array(data)
            p, d, q = order
            
            # 差分处理
            diff_data = ts_data.copy()
            for _ in range(d):
                if len(diff_data) <= 1:
                    raise TimeSeriesError("差分次数过多，数据不足")
                diff_data = np.diff(diff_data)
            
            # 简化的AR模型实现
            if len(diff_data) <= p:
                raise TimeSeriesError("数据长度不足以拟合指定的AR阶数")
            
            # 估计AR系数 (使用最小二乘法)
            ar_coeffs = self._estimate_ar_coefficients(diff_data, p)
            
            # 计算拟合值和残差
            fitted_values = []
            residuals = []
            
            for i in range(p, len(diff_data)):
                # AR预测
                prediction = sum(ar_coeffs[j] * diff_data[i-j-1] for j in range(p))
                fitted_values.append(prediction)
                residuals.append(diff_data[i] - prediction)
            
            # 存储模型
            self.model = {
                'order': order,
                'ar_coeffs': ar_coeffs,
                'original_data': ts_data,
                'diff_data': diff_data,
                'fitted_values': fitted_values,
                'residuals': residuals
            }
            
            return True
            
        except Exception as e:
            raise TimeSeriesError(f"ARIMA模型拟合失败: {str(e)}")
    
    def predict_future_values(self, steps: int, confidence_level: float = 0.95) -> Dict[str, Any]:
        """
        预测未来值
        
        Args:
            steps: 预测步数
            confidence_level: 置信水平
            
        Returns:
            Dict[str, Any]: 预测结果
                - predictions: 预测值列表
                - confidence_intervals: 置信区间列表
                - forecast_dates: 预测日期列表
                
        Raises:
            TimeSeriesError: 模型未拟合时抛出
        """
        if self.model is None:
            raise TimeSeriesError("模型尚未拟合，请先调用fit_arima_model")
        
        if steps <= 0:
            raise TimeSeriesError("预测步数必须大于0")
        
        try:
            p, d, q = self.model['order']
            ar_coeffs = self.model['ar_coeffs']
            diff_data = self.model['diff_data']
            residuals = self.model['residuals']
            
            # 预测差分后的值
            predictions = []
            last_values = diff_data[-p:].tolist()  # 最后p个值
            
            for _ in range(steps):
                # AR预测
                pred = sum(ar_coeffs[j] * last_values[-j-1] for j in range(p))
                predictions.append(pred)
                last_values.append(pred)
                last_values = last_values[-p:]  # 保持窗口大小
            
            # 反差分处理 (简化版本)
            if d > 0:
                # 这里简化处理，实际应该进行完整的反差分
                original_data = self.model['original_data']
                last_original = original_data[-1]
                
                # 简单累加处理
                final_predictions = []
                for pred in predictions:
                    last_original += pred
                    final_predictions.append(last_original)
                predictions = final_predictions
            
            # 计算置信区间 (简化版本)
            if residuals:
                residual_std = np.std(residuals)
                z_score = 1.96 if confidence_level == 0.95 else 1.645  # 简化处理
                
                confidence_intervals = []
                for pred in predictions:
                    margin = z_score * residual_std
                    confidence_intervals.append((pred - margin, pred + margin))
            else:
                confidence_intervals = [(pred, pred) for pred in predictions]
            
            # 生成预测日期 (简化版本)
            forecast_dates = [f"T+{i+1}" for i in range(steps)]
            
            return {
                'predictions': predictions,
                'confidence_intervals': confidence_intervals,
                'forecast_dates': forecast_dates
            }
            
        except Exception as e:
            raise TimeSeriesError(f"预测失败: {str(e)}")
    
    def decompose_seasonal(self, data: List[float], period: int = 24) -> Dict[str, List[float]]:
        """
        季节性分解
        
        Args:
            data: 时间序列数据
            period: 季节周期 (小时数，默认24小时)
            
        Returns:
            Dict[str, List[float]]: 分解结果
                - trend: 趋势成分
                - seasonal: 季节性成分
                - residual: 残差成分
                - original: 原始数据
        """
        if len(data) < period * 2:
            raise TimeSeriesError(f"数据长度不足，至少需要 {period * 2} 个数据点")
        
        data_array = np.array(data)
        
        # 计算趋势成分 (使用移动平均)
        trend = self._calculate_trend(data_array, period)
        
        # 去趋势
        detrended = data_array - np.array(trend)
        
        # 计算季节性成分
        seasonal = self._calculate_seasonal(detrended, period)
        
        # 计算残差
        residual = detrended - np.array(seasonal)
        
        return {
            'trend': trend,
            'seasonal': seasonal,
            'residual': residual.tolist(),
            'original': data
        }
    
    def _calculate_trend(self, data: np.ndarray, period: int) -> List[float]:
        """计算趋势成分"""
        # 使用中心移动平均
        trend = []
        half_period = period // 2
        
        for i in range(len(data)):
            if i < half_period:
                # 前半部分使用前向平均
                trend.append(np.mean(data[:i+half_period+1]))
            elif i >= len(data) - half_period:
                # 后半部分使用后向平均
                trend.append(np.mean(data[i-half_period:]))
            else:
                # 中间部分使用中心平均
                trend.append(np.mean(data[i-half_period:i+half_period+1]))
        
        return trend
    
    def _calculate_seasonal(self, detrended: np.ndarray, period: int) -> List[float]:
        """计算季节性成分"""
        seasonal = np.zeros(len(detrended))
        
        # 计算每个季节位置的平均值
        seasonal_averages = np.zeros(period)
        seasonal_counts = np.zeros(period)
        
        for i, value in enumerate(detrended):
            season_idx = i % period
            seasonal_averages[season_idx] += value
            seasonal_counts[season_idx] += 1
        
        # 避免除零
        seasonal_counts[seasonal_counts == 0] = 1
        seasonal_averages = seasonal_averages / seasonal_counts
        
        # 分配季节性成分
        for i in range(len(detrended)):
            seasonal[i] = seasonal_averages[i % period]
        
        return seasonal.tolist()
    
    def detect_trend(self, data: List[float], window_size: int = 7) -> Dict[str, Any]:
        """
        检测数据趋势
        
        Args:
            data: 时间序列数据
            window_size: 移动平均窗口大小
            
        Returns:
            Dict[str, Any]: 趋势分析结果
                - trend_direction: 趋势方向 ('increasing', 'decreasing', 'stable')
                - trend_strength: 趋势强度 (0-1)
                - trend_line: 趋势线数据
                - change_points: 趋势变化点
        """
        pass
    
    def identify_patterns(self, data: List[float]) -> Dict[str, Any]:
        """
        识别时间序列模式
        
        Args:
            data: 时间序列数据
            
        Returns:
            Dict[str, Any]: 模式识别结果
                - daily_pattern: 日内模式
                - weekly_pattern: 周模式
                - peak_hours: 高峰时段
                - low_hours: 低谷时段
                - pattern_strength: 模式强度
        """
        pass
    
    def calculate_forecast_accuracy(self, actual: List[float], predicted: List[float]) -> Dict[str, float]:
        """
        计算预测准确性指标
        
        Args:
            actual: 实际值
            predicted: 预测值
            
        Returns:
            Dict[str, float]: 准确性指标
                - mae: 平均绝对误差
                - mse: 均方误差
                - rmse: 均方根误差
                - mape: 平均绝对百分比误差
                - r2: 决定系数
        """
        if len(actual) != len(predicted):
            raise TimeSeriesError("实际值和预测值长度不匹配")
        
        if len(actual) == 0:
            raise TimeSeriesError("数据不能为空")
        
        actual_array = np.array(actual)
        predicted_array = np.array(predicted)
        
        # 平均绝对误差
        mae = np.mean(np.abs(actual_array - predicted_array))
        
        # 均方误差
        mse = np.mean((actual_array - predicted_array) ** 2)
        
        # 均方根误差
        rmse = np.sqrt(mse)
        
        # 平均绝对百分比误差
        # 避免除零
        non_zero_mask = actual_array != 0
        if np.any(non_zero_mask):
            mape = np.mean(np.abs((actual_array[non_zero_mask] - predicted_array[non_zero_mask]) / actual_array[non_zero_mask])) * 100
        else:
            mape = float('inf')
        
        # 决定系数 R²
        ss_res = np.sum((actual_array - predicted_array) ** 2)
        ss_tot = np.sum((actual_array - np.mean(actual_array)) ** 2)
        
        if ss_tot == 0:
            r2 = 1.0 if ss_res == 0 else 0.0
        else:
            r2 = 1 - (ss_res / ss_tot)
        
        return {
            'mae': float(mae),
            'mse': float(mse),
            'rmse': float(rmse),
            'mape': float(mape),
            'r2': float(r2)
        }
    
    def auto_select_arima_order(self, data: List[float], max_p: int = 3, 
                               max_d: int = 2, max_q: int = 3) -> Tuple[int, int, int]:
        """
        自动选择最优ARIMA参数
        
        Args:
            data: 时间序列数据
            max_p: p的最大值
            max_d: d的最大值
            max_q: q的最大值
            
        Returns:
            Tuple[int, int, int]: 最优的(p, d, q)参数组合
        """
        pass
    
    def handle_missing_values(self, data: List[Optional[float]], method: str = 'interpolation') -> List[float]:
        """
        处理缺失值
        
        Args:
            data: 包含缺失值的数据
            method: 处理方法 ('interpolation', 'forward_fill', 'backward_fill', 'mean')
            
        Returns:
            List[float]: 处理后的数据
        """
        pass
    
    def detect_outliers(self, data: List[float], method: str = 'iqr', threshold: float = 1.5) -> List[int]:
        """
        检测异常值
        
        Args:
            data: 时间序列数据
            method: 检测方法 ('iqr', 'zscore', 'isolation_forest')
            threshold: 异常值阈值
            
        Returns:
            List[int]: 异常值索引列表
        """
        pass
    
    def smooth_data(self, data: List[float], method: str = 'moving_average', 
                   window: int = 3) -> List[float]:
        """
        数据平滑处理
        
        Args:
            data: 原始数据
            method: 平滑方法 ('moving_average', 'exponential', 'savgol')
            window: 窗口大小
            
        Returns:
            List[float]: 平滑后的数据
        """
        if not data:
            return []
        
        data_array = np.array(data)
        
        if method == 'moving_average':
            return self._moving_average_smooth(data_array, window)
        elif method == 'exponential':
            return self._exponential_smooth(data_array, alpha=0.3)
        else:
            # 默认使用移动平均
            return self._moving_average_smooth(data_array, window)
    
    def _estimate_ar_coefficients(self, data: np.ndarray, p: int) -> List[float]:
        """估计AR系数"""
        if len(data) <= p:
            raise TimeSeriesError("数据长度不足")
        
        # 构建设计矩阵
        X = []
        y = []
        
        for i in range(p, len(data)):
            X.append([data[i-j-1] for j in range(p)])
            y.append(data[i])
        
        X = np.array(X)
        y = np.array(y)
        
        # 最小二乘估计
        try:
            coeffs = np.linalg.lstsq(X, y, rcond=None)[0]
            return coeffs.tolist()
        except np.linalg.LinAlgError:
            # 如果矩阵奇异，使用简单平均
            return [1.0 / p] * p
    
    def _moving_average_smooth(self, data: np.ndarray, window: int) -> List[float]:
        """移动平均平滑"""
        if window <= 0:
            return data.tolist()
        
        smoothed = []
        for i in range(len(data)):
            start = max(0, i - window // 2)
            end = min(len(data), i + window // 2 + 1)
            smoothed.append(np.mean(data[start:end]))
        
        return smoothed
    
    def _exponential_smooth(self, data: np.ndarray, alpha: float = 0.3) -> List[float]:
        """指数平滑"""
        if len(data) == 0:
            return []
        
        smoothed = [data[0]]
        for i in range(1, len(data)):
            smoothed.append(alpha * data[i] + (1 - alpha) * smoothed[-1])
        
        return smoothed
    
    def generate_forecast_intervals(self, predictions: List[float], 
                                  confidence_levels: List[float] = [0.8, 0.95]) -> Dict[str, List[Tuple[float, float]]]:
        """
        生成预测区间
        
        Args:
            predictions: 预测值
            confidence_levels: 置信水平列表
            
        Returns:
            Dict[str, List[Tuple[float, float]]]: 不同置信水平的预测区间
        """
        pass 