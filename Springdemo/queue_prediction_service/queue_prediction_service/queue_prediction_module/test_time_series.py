#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from src.algorithms.time_series_analysis import TimeSeriesAnalyzer

def generate_sample_data():
    """生成示例时间序列数据"""
    # 生成带有趋势和季节性的数据
    np.random.seed(42)
    n_points = 100
    
    # 趋势成分
    trend = np.linspace(10, 50, n_points)
    
    # 季节性成分 (24小时周期)
    seasonal = 10 * np.sin(2 * np.pi * np.arange(n_points) / 24)
    
    # 随机噪声
    noise = np.random.normal(0, 2, n_points)
    
    # 组合数据
    data = trend + seasonal + noise
    
    return data.tolist()

def test_time_series_analysis():
    """测试时间序列分析功能"""
    
    print('=== 时间序列分析测试 ===')
    
    # 创建分析器实例
    analyzer = TimeSeriesAnalyzer()
    
    # 生成测试数据
    data = generate_sample_data()
    print(f'\n生成测试数据: {len(data)} 个数据点')
    print(f'数据范围: {min(data):.2f} - {max(data):.2f}')
    
    # 1. 测试ARIMA模型拟合
    print('\n1. ARIMA模型拟合测试:')
    try:
        success = analyzer.fit_arima_model(data, order=(2, 1, 1))
        print(f'  模型拟合成功: {success}')
        
        if success:
            # 测试预测
            forecast = analyzer.predict_future_values(steps=5)
            print(f'  预测未来5个时间点:')
            for i, (pred, (lower, upper)) in enumerate(zip(forecast['predictions'], forecast['confidence_intervals'])):
                print(f'    T+{i+1}: {pred:.2f} (置信区间: {lower:.2f} - {upper:.2f})')
    except Exception as e:
        print(f'  错误: {e}')
    
    # 2. 测试季节性分解
    print('\n2. 季节性分解测试:')
    try:
        decomposition = analyzer.decompose_seasonal(data, period=24)
        print(f'  分解成功!')
        print(f'  趋势成分范围: {min(decomposition["trend"]):.2f} - {max(decomposition["trend"]):.2f}')
        print(f'  季节性成分范围: {min(decomposition["seasonal"]):.2f} - {max(decomposition["seasonal"]):.2f}')
        print(f'  残差成分标准差: {np.std(decomposition["residual"]):.2f}')
    except Exception as e:
        print(f'  错误: {e}')
    
    # 3. 测试数据平滑
    print('\n3. 数据平滑测试:')
    try:
        # 移动平均平滑
        smoothed_ma = analyzer.smooth_data(data, method='moving_average', window=5)
        print(f'  移动平均平滑: 原始数据标准差 {np.std(data):.2f} -> 平滑后 {np.std(smoothed_ma):.2f}')
        
        # 指数平滑
        smoothed_exp = analyzer.smooth_data(data, method='exponential')
        print(f'  指数平滑: 原始数据标准差 {np.std(data):.2f} -> 平滑后 {np.std(smoothed_exp):.2f}')
    except Exception as e:
        print(f'  错误: {e}')
    
    # 4. 测试预测准确性
    print('\n4. 预测准确性测试:')
    try:
        # 使用部分数据作为"实际值"和"预测值"
        actual = data[:50]
        predicted = [x + np.random.normal(0, 1) for x in actual]  # 添加一些预测误差
        
        accuracy = analyzer.calculate_forecast_accuracy(actual, predicted)
        print(f'  平均绝对误差 (MAE): {accuracy["mae"]:.2f}')
        print(f'  均方根误差 (RMSE): {accuracy["rmse"]:.2f}')
        print(f'  平均绝对百分比误差 (MAPE): {accuracy["mape"]:.2f}%')
        print(f'  决定系数 (R²): {accuracy["r2"]:.3f}')
    except Exception as e:
        print(f'  错误: {e}')
    
    # 5. 测试餐厅场景数据
    print('\n5. 餐厅场景数据测试:')
    try:
        # 模拟餐厅一天的人流量数据 (每小时)
        restaurant_data = [
            2, 1, 1, 0, 0, 0,  # 0-5点 (深夜)
            1, 3, 8, 15, 12, 25,  # 6-11点 (早餐和上午)
            35, 40, 30, 20, 15, 18,  # 12-17点 (午餐和下午)
            25, 45, 50, 35, 20, 10,  # 18-23点 (晚餐和夜晚)
        ]
        
        print(f'  餐厅24小时人流量数据: {restaurant_data}')
        
        # 季节性分解
        decomp = analyzer.decompose_seasonal(restaurant_data * 3, period=24)  # 重复3天的数据
        print(f'  季节性分解完成')
        
        # 数据平滑
        smoothed = analyzer.smooth_data(restaurant_data, method='moving_average', window=3)
        print(f'  平滑后的人流量: {[round(x, 1) for x in smoothed[:12]]}... (显示前12小时)')
        
    except Exception as e:
        print(f'  错误: {e}')
    
    print('\n=== 时间序列分析测试完成! ===')

if __name__ == '__main__':
    test_time_series_analysis() 