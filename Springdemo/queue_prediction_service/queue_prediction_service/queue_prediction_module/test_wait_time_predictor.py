#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from src.predictors.wait_time_predictor import WaitTimePredictor
from src.models.prediction_models import QueueData, RestaurantConfig, PredictionContext

def create_sample_data():
    """创建测试数据"""
    
    # 创建队列数据
    queue_data = QueueData(
        current_queue_length=8,
        average_service_time=20.0,  # 平均服务时间20分钟
        active_servers=2,
        timestamp=datetime.now()
    )
    
    # 创建餐厅配置
    restaurant_config = RestaurantConfig(
        restaurant_type="casual_dining",
        max_capacity=100,
        table_count=20,
        operating_hours=(9, 22),
        peak_hours=[11, 12, 18, 19, 20]
    )
    
    # 创建预测上下文
    context = PredictionContext(
        current_time=datetime(2024, 1, 15, 12, 30),  # 周一中午12:30
        weather_info={"condition": "sunny", "temperature": 25},
        is_holiday=False,
        local_events=[],
        special_conditions=[]
    )
    
    return queue_data, restaurant_config, context

def test_wait_time_predictor():
    """测试等待时间预测器"""
    
    print('=== 等待时间预测器测试 ===')
    
    # 创建预测器实例
    predictor = WaitTimePredictor()
    
    # 创建测试数据
    queue_data, restaurant_config, context = create_sample_data()
    
    print(f'\n测试场景设置:')
    print(f'  当前队列长度: {queue_data.current_queue_length}')
    print(f'  活跃服务台: {queue_data.active_servers}')
    print(f'  平均服务时间: {queue_data.average_service_time} 分钟')
    print(f'  餐厅类型: {restaurant_config.restaurant_type}')
    print(f'  预测时间: {context.current_time}')
    
    # 1. 测试基本预测功能
    print('\n1. 基本等待时间预测测试:')
    try:
        input_data = {
            'queue_data': queue_data,
            'customer_position': 9,  # 新顾客排在第9位
            'restaurant_config': restaurant_config
        }
        
        prediction = predictor.predict(input_data, context)
        
        print(f'  预测结果:')
        print(f'    预计等待时间: {prediction.estimated_wait_time:.1f} 分钟')
        print(f'    置信度: {prediction.confidence_level:.2f}')
        print(f'    队列位置: {prediction.customer_position}')
        print(f'    预测范围: {prediction.prediction_range[0]:.1f} - {prediction.prediction_range[1]:.1f} 分钟')
        print(f'    顾客提示: {prediction.message}')
        
    except Exception as e:
        print(f'  错误: {e}')
    
    # 2. 测试不同时段的预测
    print('\n2. 不同时段预测测试:')
    test_times = [
        (datetime(2024, 1, 15, 8, 0), "早晨"),
        (datetime(2024, 1, 15, 12, 0), "午餐高峰"),
        (datetime(2024, 1, 15, 15, 0), "下午低谷"),
        (datetime(2024, 1, 15, 19, 0), "晚餐高峰"),
        (datetime(2024, 1, 15, 22, 0), "夜晚")
    ]
    
    for test_time, period_name in test_times:
        try:
            test_context = PredictionContext(
                current_time=test_time,
                weather_info={"condition": "sunny"},
                is_holiday=False,
                local_events=[],
                special_conditions=[]
            )
            
            input_data = {
                'queue_data': queue_data,
                'customer_position': 5,
                'restaurant_config': restaurant_config
            }
            
            prediction = predictor.predict(input_data, test_context)
            print(f'  {period_name} ({test_time.hour}:00): {prediction.estimated_wait_time:.1f}分钟 (置信度: {prediction.confidence_level:.2f})')
            
        except Exception as e:
            print(f'  {period_name} 预测错误: {e}')
    
    # 3. 测试冷启动情况
    print('\n3. 冷启动预测测试:')
    try:
        # 创建新的预测器实例 (模拟冷启动)
        cold_start_predictor = WaitTimePredictor()
        
        input_data = {
            'queue_data': queue_data,
            'customer_position': 6,
            'restaurant_config': restaurant_config
        }
        
        prediction = cold_start_predictor.predict(input_data, context)
        print(f'  冷启动预测:')
        print(f'    等待时间: {prediction.estimated_wait_time:.1f} 分钟')
        print(f'    置信度: {prediction.confidence_level:.2f}')
        
    except Exception as e:
        print(f'  冷启动预测错误: {e}')
    
    # 4. 测试不同队列长度的预测
    print('\n4. 不同队列长度预测测试:')
    queue_lengths = [0, 3, 8, 15, 25]
    
    for length in queue_lengths:
        try:
            test_queue = QueueData(
                current_queue_length=length,
                average_service_time=20.0,
                active_servers=2,
                timestamp=datetime.now()
            )
            
            input_data = {
                'queue_data': test_queue,
                'customer_position': length + 1,
                'restaurant_config': restaurant_config
            }
            
            prediction = predictor.predict(input_data, context)
            print(f'  队列长度 {length}: 等待时间 {prediction.estimated_wait_time:.1f}分钟')
            
        except Exception as e:
            print(f'  队列长度 {length} 预测错误: {e}')
    
    # 5. 测试实时数据更新
    print('\n5. 实时数据更新测试:')
    try:
        # 模拟一些预测和实际结果
        test_cases = [
            (15.0, 18.0),  # 预测15分钟，实际18分钟
            (10.0, 8.0),   # 预测10分钟，实际8分钟
            (25.0, 22.0),  # 预测25分钟，实际22分钟
        ]
        
        for predicted, actual in test_cases:
            predictor.update_real_time_data(actual, predicted)
            error = abs(actual - predicted)
            print(f'  预测: {predicted}分钟, 实际: {actual}分钟, 误差: {error:.1f}分钟')
        
        print(f'  预测历史记录数: {len(predictor.prediction_history)}')
        
        if predictor.prediction_history:
            avg_accuracy = sum(record['accuracy'] for record in predictor.prediction_history) / len(predictor.prediction_history)
            print(f'  平均预测准确率: {avg_accuracy:.2f}')
        
    except Exception as e:
        print(f'  实时更新测试错误: {e}')
    
    # 6. 测试不同餐厅类型
    print('\n6. 不同餐厅类型预测测试:')
    restaurant_types = ['fast_food', 'casual_dining', 'fine_dining']
    
    for rest_type in restaurant_types:
        try:
            test_config = RestaurantConfig(
                restaurant_type=rest_type,
                max_capacity=80,
                table_count=15,
                operating_hours=(9, 22),
                peak_hours=[11, 12, 18, 19, 20]
            )
            
            input_data = {
                'queue_data': queue_data,
                'customer_position': 5,
                'restaurant_config': test_config
            }
            
            prediction = predictor.predict(input_data, context)
            print(f'  {rest_type}: {prediction.estimated_wait_time:.1f}分钟')
            
        except Exception as e:
            print(f'  {rest_type} 预测错误: {e}')
    
    print('\n=== 等待时间预测器测试完成! ===')

if __name__ == '__main__':
    test_wait_time_predictor() 