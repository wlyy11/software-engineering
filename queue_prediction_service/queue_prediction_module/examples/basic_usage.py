"""
餐厅排队预测系统 - 基本使用示例
演示如何使用预测API进行等待时间和人流量预测
"""

from datetime import datetime, timedelta
import sys
import os

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from interfaces.prediction_api import PredictionAPI
from models.prediction_models import (
    QueueData, RestaurantConfig, HistoricalData, PredictionContext
)


def example_wait_time_prediction():
    """
    示例：预测顾客等待时间
    """
    print("=== 顾客等待时间预测示例 ===")
    
    # 初始化预测API
    api = PredictionAPI()
    
    # 创建当前排队数据
    queue_data = QueueData(
        current_queue_length=15,
        average_service_time=8.0,  # 8分钟
        active_servers=3,
        timestamp=datetime.now()
    )
    
    # 创建餐厅配置
    restaurant_config = RestaurantConfig(
        restaurant_type='fast_food',
        max_capacity=100,
        table_count=20,
        operating_hours=(7, 22),  # 7:00-22:00
        peak_hours=[12, 13, 18, 19]
    )
    
    # 创建预测上下文
    context = PredictionContext(
        current_time=datetime.now(),
        weather_info={'temperature': 25, 'weather_type': 'sunny'},
        is_holiday=False,
        local_events=[],
        special_conditions=[]
    )
    
    try:
        # 预测第10位顾客的等待时间
        customer_position = 10
        prediction = api.predict_customer_wait_time(
            queue_data=queue_data,
            customer_position=customer_position,
            restaurant_config=restaurant_config,
            context=context
        )
        
        print(f"顾客位置: 第{customer_position}位")
        print(f"预计等待时间: {prediction.estimated_wait_time:.1f} 分钟")
        print(f"时间范围: {prediction.prediction_range[0]:.1f} - {prediction.prediction_range[1]:.1f} 分钟")
        print(f"预测置信度: {prediction.confidence_level:.2f}")
        print(f"提示信息: {prediction.message}")
        
    except Exception as e:
        print(f"预测失败: {e}")


def example_traffic_prediction():
    """
    示例：预测人流量趋势
    """
    print("\n=== 人流量趋势预测示例 ===")
    
    # 初始化预测API
    api = PredictionAPI()
    
    # 创建餐厅配置
    restaurant_config = RestaurantConfig(
        restaurant_type='casual_dining',
        max_capacity=150,
        table_count=30,
        operating_hours=(11, 23),  # 11:00-23:00
        peak_hours=[12, 13, 18, 19, 20]
    )
    
    # 创建预测上下文
    context = PredictionContext(
        current_time=datetime.now(),
        weather_info={'temperature': 22, 'weather_type': 'cloudy'},
        is_holiday=False,
        local_events=['附近商场促销活动'],
        special_conditions=[]
    )
    
    try:
        # 预测未来24小时人流量
        current_traffic = 35
        prediction = api.predict_traffic_trends(
            current_traffic=current_traffic,
            restaurant_config=restaurant_config,
            prediction_hours=24,
            context=context
        )
        
        print(f"当前人流量: {current_traffic} 人")
        print(f"预测时长: {prediction.prediction_horizon} 小时")
        print(f"预测时段数: {len(prediction.time_slots)}")
        
        # 显示高峰时段
        print("\n高峰时段预测:")
        for peak in prediction.peak_periods:
            print(f"  {peak['time']}: {peak['predicted_customers']} 人 ({peak['intensity']})")
        
        # 显示部分预测数据
        print("\n未来6小时预测:")
        for i in range(min(6, len(prediction.time_slots))):
            time_slot = prediction.time_slots[i]
            traffic = prediction.predicted_traffic[i]
            confidence = prediction.confidence_intervals[i]
            print(f"  {time_slot}: {traffic} 人 (置信区间: {confidence[0]}-{confidence[1]})")
            
    except Exception as e:
        print(f"预测失败: {e}")


def example_system_initialization():
    """
    示例：系统初始化
    """
    print("\n=== 系统初始化示例 ===")
    
    # 创建历史数据 (模拟数据)
    historical_data = HistoricalData(
        hourly_traffic={'2024-01-01': [5, 3, 2, 2, 3, 5, 8, 12, 15, 18, 25, 35, 45, 35, 20, 15, 12, 25, 40, 35, 20, 15, 10, 8]},
        daily_patterns={'monday': [5, 8, 12, 15, 20, 25, 30, 35, 40, 35, 30, 25, 20, 15, 12, 10, 8, 15, 25, 30, 25, 20, 15, 10]},
        weekly_patterns=[1.0, 0.8, 0.9, 1.1, 1.2, 1.5, 1.3],  # 周一到周日的倍数
        seasonal_factors={'spring': 1.0, 'summer': 1.2, 'autumn': 1.1, 'winter': 0.9},
        external_factors={'weather_impact': 0.1, 'holiday_impact': 0.3}
    )
    
    # 创建餐厅配置
    restaurant_config = RestaurantConfig(
        restaurant_type='casual_dining',
        max_capacity=120,
        table_count=25,
        operating_hours=(10, 22),
        peak_hours=[12, 13, 18, 19, 20]
    )
    
    # 初始化预测系统
    api = PredictionAPI()
    
    try:
        success = api.initialize_system(historical_data, restaurant_config)
        if success:
            print("✅ 预测系统初始化成功")
            
            # 获取系统状态
            status = api.get_system_status()
            print(f"系统状态: {status}")
            
        else:
            print("❌ 预测系统初始化失败")
            
    except Exception as e:
        print(f"初始化失败: {e}")


def main():
    """
    主函数 - 运行所有示例
    """
    print("餐厅排队预测系统 - 使用示例")
    print("=" * 50)
    
    # 运行各个示例
    example_system_initialization()
    example_wait_time_prediction()
    example_traffic_prediction()
    
    print("\n" + "=" * 50)
    print("示例运行完成")


if __name__ == "__main__":
    main() 