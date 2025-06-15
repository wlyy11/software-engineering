#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from src.predictors.traffic_predictor import TrafficPredictor
from src.models.prediction_models import RestaurantConfig, PredictionContext

def create_test_data():
    """创建测试数据"""
    
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
        current_time=datetime(2024, 1, 15, 10, 0),  # 周一上午10点
        weather_info={"condition": "sunny", "temperature": 22},
        is_holiday=False,
        local_events=[],
        special_conditions=[]
    )
    
    return restaurant_config, context

def test_traffic_predictor():
    """测试人流量预测器"""
    
    print('=== 人流量预测器测试 ===')
    
    # 创建预测器实例
    predictor = TrafficPredictor()
    
    # 创建测试数据
    restaurant_config, context = create_test_data()
    
    print(f'\n测试场景设置:')
    print(f'  餐厅类型: {restaurant_config.restaurant_type}')
    print(f'  最大容量: {restaurant_config.max_capacity}')
    print(f'  预测时间: {context.current_time}')
    print(f'  天气条件: {context.weather_info["condition"]}')
    print(f'  是否节假日: {context.is_holiday}')
    
    # 1. 测试基本人流量预测
    print('\n1. 基本人流量预测测试 (24小时):')
    try:
        input_data = {
            'current_traffic': 15,
            'prediction_hours': 24,
            'restaurant_config': restaurant_config
        }
        
        prediction = predictor.predict(input_data, context)
        
        print(f'  预测结果:')
        print(f'    预测时长: {prediction.prediction_horizon} 小时')
        print(f'    时间段数: {len(prediction.time_slots)}')
        print(f'    预测人流范围: {min(prediction.predicted_traffic)} - {max(prediction.predicted_traffic)} 人/小时')
        print(f'    平均人流: {sum(prediction.predicted_traffic) / len(prediction.predicted_traffic):.1f} 人/小时')
        print(f'    识别的高峰期数量: {len(prediction.peak_periods)}')
        
        # 显示前12小时的详细预测
        print(f'\n  前12小时详细预测:')
        for i in range(min(12, len(prediction.time_slots))):
            time_slot = prediction.time_slots[i]
            traffic = prediction.predicted_traffic[i]
            confidence = prediction.confidence_intervals[i]
            print(f'    {time_slot}: {traffic} 人 (置信区间: {confidence[0]}-{confidence[1]})')
        
        # 显示高峰期信息
        if prediction.peak_periods:
            print(f'\n  高峰期详情:')
            for i, period in enumerate(prediction.peak_periods):
                print(f'    高峰期 {i+1}: {period["start_time"]} - {period["end_time"]}')
                print(f'      持续时长: {period["duration_hours"]} 小时')
                print(f'      峰值人流: {period["peak_traffic"]} 人')
                print(f'      平均人流: {period["avg_traffic"]:.1f} 人')
        
    except Exception as e:
        print(f'  错误: {e}')
    
    # 2. 测试不同餐厅类型的预测
    print('\n2. 不同餐厅类型预测测试:')
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
                'current_traffic': 10,
                'prediction_hours': 12,
                'restaurant_config': test_config
            }
            
            prediction = predictor.predict(input_data, context)
            avg_traffic = sum(prediction.predicted_traffic) / len(prediction.predicted_traffic)
            max_traffic = max(prediction.predicted_traffic)
            
            print(f'  {rest_type}:')
            print(f'    平均人流: {avg_traffic:.1f} 人/小时')
            print(f'    峰值人流: {max_traffic} 人/小时')
            print(f'    高峰期数: {len(prediction.peak_periods)}')
            
        except Exception as e:
            print(f'  {rest_type} 预测错误: {e}')
    
    # 3. 测试不同天气条件的影响
    print('\n3. 天气条件影响测试:')
    weather_conditions = [
        {"condition": "sunny", "temperature": 25},
        {"condition": "rainy", "temperature": 18},
        {"condition": "cloudy", "temperature": 20}
    ]
    
    for weather in weather_conditions:
        try:
            test_context = PredictionContext(
                current_time=datetime(2024, 1, 15, 12, 0),
                weather_info=weather,
                is_holiday=False,
                local_events=[],
                special_conditions=[]
            )
            
            input_data = {
                'current_traffic': 20,
                'prediction_hours': 8,
                'restaurant_config': restaurant_config
            }
            
            prediction = predictor.predict(input_data, test_context)
            avg_traffic = sum(prediction.predicted_traffic) / len(prediction.predicted_traffic)
            
            print(f'  {weather["condition"]} 天气: 平均人流 {avg_traffic:.1f} 人/小时')
            
        except Exception as e:
            print(f'  {weather["condition"]} 天气预测错误: {e}')
    
    # 4. 测试节假日影响
    print('\n4. 节假日影响测试:')
    try:
        # 普通日
        normal_context = PredictionContext(
            current_time=datetime(2024, 1, 15, 12, 0),
            weather_info={"condition": "sunny"},
            is_holiday=False,
            local_events=[],
            special_conditions=[]
        )
        
        # 节假日
        holiday_context = PredictionContext(
            current_time=datetime(2024, 1, 15, 12, 0),
            weather_info={"condition": "sunny"},
            is_holiday=True,
            local_events=[],
            special_conditions=[]
        )
        
        input_data = {
            'current_traffic': 25,
            'prediction_hours': 8,
            'restaurant_config': restaurant_config
        }
        
        normal_prediction = predictor.predict(input_data, normal_context)
        holiday_prediction = predictor.predict(input_data, holiday_context)
        
        normal_avg = sum(normal_prediction.predicted_traffic) / len(normal_prediction.predicted_traffic)
        holiday_avg = sum(holiday_prediction.predicted_traffic) / len(holiday_prediction.predicted_traffic)
        
        print(f'  普通日平均人流: {normal_avg:.1f} 人/小时')
        print(f'  节假日平均人流: {holiday_avg:.1f} 人/小时')
        print(f'  节假日增幅: {((holiday_avg - normal_avg) / normal_avg * 100):.1f}%')
        
    except Exception as e:
        print(f'  节假日影响测试错误: {e}')
    
    # 5. 测试经营洞察生成
    print('\n5. 经营洞察生成测试:')
    try:
        input_data = {
            'current_traffic': 30,
            'prediction_hours': 24,
            'restaurant_config': restaurant_config
        }
        
        prediction = predictor.predict(input_data, context)
        insights = predictor.get_business_insights(prediction)
        
        print(f'  经营洞察:')
        
        if insights['staffing_recommendations']:
            print(f'    人员配置建议:')
            for rec in insights['staffing_recommendations'][:3]:  # 显示前3条
                print(f'      - {rec}')
        
        if insights['operational_tips']:
            print(f'    运营建议:')
            for tip in insights['operational_tips']:
                print(f'      - {tip}')
        
        if insights['revenue_opportunities']:
            print(f'    收入机会:')
            for opp in insights['revenue_opportunities']:
                print(f'      - {opp}')
        
    except Exception as e:
        print(f'  经营洞察生成错误: {e}')
    
    # 6. 测试图表数据生成
    print('\n6. 图表数据生成测试:')
    try:
        input_data = {
            'current_traffic': 20,
            'prediction_hours': 12,
            'restaurant_config': restaurant_config
        }
        
        prediction = predictor.predict(input_data, context)
        chart_data = prediction.chart_data
        
        print(f'  图表数据:')
        print(f'    图表类型: {chart_data["type"]}')
        print(f'    标题: {chart_data["title"]}')
        print(f'    数据点数量: {len(chart_data["x_axis"]["data"])}')
        print(f'    统计信息:')
        stats = chart_data["statistics"]
        print(f'      最大人流: {stats["max_traffic"]} 人')
        print(f'      最小人流: {stats["min_traffic"]} 人')
        print(f'      平均人流: {stats["avg_traffic"]:.1f} 人')
        print(f'      高峰期数: {stats["total_peaks"]}')
        
    except Exception as e:
        print(f'  图表数据生成错误: {e}')
    
    print('\n=== 人流量预测器测试完成! ===')

if __name__ == '__main__':
    test_traffic_predictor() 