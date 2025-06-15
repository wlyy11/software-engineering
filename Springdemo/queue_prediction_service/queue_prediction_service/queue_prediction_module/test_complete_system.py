#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
餐厅排队预测系统 - 完整系统测试
展示所有核心功能的集成测试
"""

from datetime import datetime, timedelta
from src.algorithms.queue_theory import QueueTheoryCalculator
from src.algorithms.time_series_analysis import TimeSeriesAnalyzer
from src.predictors.wait_time_predictor import WaitTimePredictor
from src.predictors.traffic_predictor import TrafficPredictor
from src.models.prediction_models import QueueData, RestaurantConfig, PredictionContext
import numpy as np

def print_section_header(title):
    """打印章节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_subsection_header(title):
    """打印子章节标题"""
    print(f"\n{'-'*40}")
    print(f"  {title}")
    print(f"{'-'*40}")

def test_complete_system():
    """完整系统测试"""
    
    print_section_header("餐厅排队预测系统 - 完整功能演示")
    
    # 创建测试场景
    print("\n🏪 测试场景设置:")
    print("  餐厅名称: 美味轩中餐厅")
    print("  餐厅类型: 休闲餐饮 (casual_dining)")
    print("  营业时间: 09:00 - 22:00")
    print("  服务台数: 3个")
    print("  最大容量: 120人")
    print("  当前时间: 2024年1月15日 周一 12:30")
    print("  当前队列: 15人排队")
    print("  天气状况: 晴天 22°C")
    
    # 创建基础数据
    restaurant_config = RestaurantConfig(
        restaurant_type="casual_dining",
        max_capacity=120,
        table_count=25,
        operating_hours=(9, 22),
        peak_hours=[11, 12, 18, 19, 20]
    )
    
    queue_data = QueueData(
        current_queue_length=15,
        average_service_time=25.0,  # 25分钟平均服务时间
        active_servers=3,
        timestamp=datetime.now()
    )
    
    context = PredictionContext(
        current_time=datetime(2024, 1, 15, 12, 30),
        weather_info={"condition": "sunny", "temperature": 22},
        is_holiday=False,
        local_events=[],
        special_conditions=[]
    )
    
    # 1. 排队论算法演示
    print_section_header("1. 排队论算法核心功能")
    
    queue_calculator = QueueTheoryCalculator()
    
    print("\n📊 M/M/1 单服务台模型:")
    try:
        mm1_result = queue_calculator.calculate_mm1_wait_time(
            arrival_rate=18,  # 每小时18个顾客
            service_rate=20   # 每小时服务20个顾客
        )
        print(f"  到达率: 18 顾客/小时")
        print(f"  服务率: 20 顾客/小时")
        print(f"  平均等待时间: {mm1_result['avg_wait_time']:.1f} 分钟")
        print(f"  系统利用率: {mm1_result['utilization']:.1%}")
        print(f"  平均队列长度: {mm1_result['avg_queue_length']:.1f} 人")
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    
    print("\n📊 M/M/c 多服务台模型:")
    try:
        mmc_result = queue_calculator.calculate_mmc_wait_time(
            arrival_rate=45,  # 每小时45个顾客
            service_rate=20,  # 每个服务台每小时服务20个顾客
            servers=3         # 3个服务台
        )
        print(f"  到达率: 45 顾客/小时")
        print(f"  服务率: 20 顾客/小时/台")
        print(f"  服务台数: 3个")
        print(f"  平均等待时间: {mmc_result['avg_wait_time']:.1f} 分钟")
        print(f"  系统利用率: {mmc_result['utilization']:.1%}")
        print(f"  等待概率: {mmc_result['prob_wait']:.1%}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    
    print("\n📊 系统性能分析:")
    try:
        analysis = queue_calculator.analyze_queue_performance(
            arrival_rate=35, service_rate=15, servers=3
        )
        print(f"  系统状态: {analysis['stability_status']}")
        if analysis['performance_metrics']:
            metrics = analysis['performance_metrics']
            print(f"  平均等待时间: {metrics['avg_wait_time']:.1f} 分钟")
            print(f"  系统利用率: {metrics['utilization']:.1%}")
        print(f"  优化建议:")
        for rec in analysis['recommendations']:
            print(f"    • {rec}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    
    # 2. 时间序列分析演示
    print_section_header("2. 时间序列分析功能")
    
    ts_analyzer = TimeSeriesAnalyzer()
    
    print("\n📈 生成模拟历史数据:")
    # 生成48小时的模拟人流数据
    np.random.seed(42)
    base_pattern = [2, 1, 1, 0, 0, 1, 3, 8, 15, 25, 35, 45, 40, 30, 20, 15, 12, 20, 40, 50, 35, 25, 15, 8] * 2
    noise = np.random.normal(0, 3, len(base_pattern))
    historical_data = [max(0, int(base + n)) for base, n in zip(base_pattern, noise)]
    
    print(f"  数据长度: {len(historical_data)} 小时")
    print(f"  数据范围: {min(historical_data)} - {max(historical_data)} 人/小时")
    print(f"  平均人流: {np.mean(historical_data):.1f} 人/小时")
    
    print("\n📈 ARIMA模型拟合:")
    try:
        success = ts_analyzer.fit_arima_model(historical_data, order=(2, 1, 1))
        if success:
            print("  ✅ ARIMA模型拟合成功")
            
            # 预测未来6小时
            forecast = ts_analyzer.predict_future_values(steps=6)
            print(f"  未来6小时预测:")
            for i, (pred, (lower, upper)) in enumerate(zip(forecast['predictions'], forecast['confidence_intervals'])):
                print(f"    T+{i+1}: {pred:.1f} 人 (置信区间: {lower:.1f} - {upper:.1f})")
        else:
            print("  ❌ ARIMA模型拟合失败")
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    
    print("\n📈 季节性分解:")
    try:
        decomposition = ts_analyzer.decompose_seasonal(historical_data, period=24)
        print("  ✅ 季节性分解完成")
        print(f"  趋势成分范围: {min(decomposition['trend']):.1f} - {max(decomposition['trend']):.1f}")
        print(f"  季节性成分范围: {min(decomposition['seasonal']):.1f} - {max(decomposition['seasonal']):.1f}")
        print(f"  残差标准差: {np.std(decomposition['residual']):.1f}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    
    print("\n📈 数据平滑处理:")
    try:
        smoothed = ts_analyzer.smooth_data(historical_data, method='moving_average', window=3)
        print(f"  原始数据标准差: {np.std(historical_data):.1f}")
        print(f"  平滑后标准差: {np.std(smoothed):.1f}")
        print(f"  平滑效果: 降低了 {((np.std(historical_data) - np.std(smoothed)) / np.std(historical_data) * 100):.1f}% 的波动")
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    
    # 3. 等待时间预测演示
    print_section_header("3. 顾客等待时间预测")
    
    wait_predictor = WaitTimePredictor()
    
    print("\n⏰ 不同位置顾客的等待时间预测:")
    customer_positions = [1, 5, 10, 16]  # 新顾客排在第16位
    
    for position in customer_positions:
        try:
            input_data = {
                'queue_data': queue_data,
                'customer_position': position,
                'restaurant_config': restaurant_config
            }
            
            prediction = wait_predictor.predict(input_data, context)
            
            print(f"  第 {position} 位顾客:")
            print(f"    预计等待时间: {prediction.estimated_wait_time:.1f} 分钟")
            print(f"    置信度: {prediction.confidence_level:.1%}")
            print(f"    预测范围: {prediction.prediction_range[0]:.1f} - {prediction.prediction_range[1]:.1f} 分钟")
            print(f"    顾客提示: {prediction.message}")
            
        except Exception as e:
            print(f"    ❌ 第 {position} 位顾客预测错误: {e}")
    
    print("\n⏰ 不同时段的等待时间对比:")
    time_periods = [
        (datetime(2024, 1, 15, 8, 0), "早晨低峰"),
        (datetime(2024, 1, 15, 12, 0), "午餐高峰"),
        (datetime(2024, 1, 15, 15, 0), "下午低峰"),
        (datetime(2024, 1, 15, 19, 0), "晚餐高峰"),
        (datetime(2024, 1, 15, 22, 0), "夜晚收尾")
    ]
    
    for test_time, period_name in time_periods:
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
                'customer_position': 8,  # 统一测试第8位
                'restaurant_config': restaurant_config
            }
            
            prediction = wait_predictor.predict(input_data, test_context)
            print(f"  {period_name} ({test_time.hour}:00): {prediction.estimated_wait_time:.1f} 分钟")
            
        except Exception as e:
            print(f"  {period_name} 预测错误: {e}")
    
    # 4. 人流量预测演示
    print_section_header("4. 人流量趋势预测")
    
    traffic_predictor = TrafficPredictor()
    
    print("\n📊 未来24小时人流量预测:")
    try:
        input_data = {
            'current_traffic': 35,  # 当前35人/小时
            'prediction_hours': 24,
            'restaurant_config': restaurant_config
        }
        
        traffic_prediction = traffic_predictor.predict(input_data, context)
        
        print(f"  预测时长: {traffic_prediction.prediction_horizon} 小时")
        print(f"  预测人流范围: {min(traffic_prediction.predicted_traffic)} - {max(traffic_prediction.predicted_traffic)} 人/小时")
        print(f"  平均人流: {np.mean(traffic_prediction.predicted_traffic):.1f} 人/小时")
        print(f"  识别高峰期: {len(traffic_prediction.peak_periods)} 个")
        
        # 显示接下来8小时的详细预测
        print(f"\n  接下来8小时详细预测:")
        for i in range(8):
            time_slot = traffic_prediction.time_slots[i]
            traffic = traffic_prediction.predicted_traffic[i]
            confidence = traffic_prediction.confidence_intervals[i]
            print(f"    {time_slot}: {traffic} 人/小时 (区间: {confidence[0]}-{confidence[1]})")
        
        # 显示高峰期信息
        if traffic_prediction.peak_periods:
            print(f"\n  高峰期分析:")
            for i, period in enumerate(traffic_prediction.peak_periods):
                print(f"    高峰期 {i+1}: {period['start_time']} - {period['end_time']}")
                print(f"      持续: {period['duration_hours']} 小时")
                print(f"      峰值: {period['peak_traffic']} 人/小时")
                print(f"      平均: {period['avg_traffic']:.1f} 人/小时")
        
    except Exception as e:
        print(f"  ❌ 人流量预测错误: {e}")
    
    print("\n📊 经营决策建议:")
    try:
        insights = traffic_predictor.get_business_insights(traffic_prediction)
        
        if insights['staffing_recommendations']:
            print(f"  👥 人员配置建议:")
            for rec in insights['staffing_recommendations'][:2]:
                print(f"    • {rec}")
        
        if insights['operational_tips']:
            print(f"  💡 运营优化建议:")
            for tip in insights['operational_tips']:
                print(f"    • {tip}")
        
        if insights['revenue_opportunities']:
            print(f"  💰 收入机会:")
            for opp in insights['revenue_opportunities']:
                print(f"    • {opp}")
        
    except Exception as e:
        print(f"  ❌ 经营洞察生成错误: {e}")
    
    # 5. 系统集成演示
    print_section_header("5. 系统集成应用场景")
    
    print("\n🎯 场景1: 新顾客到店咨询等待时间")
    try:
        # 模拟新顾客询问
        new_customer_position = queue_data.current_queue_length + 1
        
        input_data = {
            'queue_data': queue_data,
            'customer_position': new_customer_position,
            'restaurant_config': restaurant_config
        }
        
        wait_prediction = wait_predictor.predict(input_data, context)
        
        print(f"  顾客询问: '现在排队大概要等多久？'")
        print(f"  系统回答: '您好！您是第 {new_customer_position} 位顾客'")
        print(f"           '预计等待时间: {wait_prediction.estimated_wait_time:.0f} 分钟'")
        print(f"           '置信度: {wait_prediction.confidence_level:.0%}'")
        print(f"           '{wait_prediction.message}'")
        
    except Exception as e:
        print(f"  ❌ 场景1错误: {e}")
    
    print("\n🎯 场景2: 经理查看今日人流预测")
    try:
        # 预测剩余营业时间的人流
        current_hour = context.current_time.hour
        remaining_hours = 22 - current_hour  # 营业到22点
        
        input_data = {
            'current_traffic': 35,
            'prediction_hours': remaining_hours,
            'restaurant_config': restaurant_config
        }
        
        manager_prediction = traffic_predictor.predict(input_data, context)
        
        print(f"  经理查询: '今天剩余时间的人流预测如何？'")
        print(f"  系统报告:")
        print(f"    • 剩余营业时间: {remaining_hours} 小时")
        print(f"    • 预计总客流: {sum(manager_prediction.predicted_traffic)} 人次")
        print(f"    • 预计高峰期: {len(manager_prediction.peak_periods)} 个")
        
        if manager_prediction.peak_periods:
            next_peak = manager_prediction.peak_periods[0]
            print(f"    • 下个高峰期: {next_peak['start_time']} - {next_peak['end_time']}")
            print(f"    • 峰值人流: {next_peak['peak_traffic']} 人/小时")
        
        # 给出具体建议
        insights = traffic_predictor.get_business_insights(manager_prediction)
        if insights['staffing_recommendations']:
            print(f"    • 人员建议: {insights['staffing_recommendations'][0]}")
        
    except Exception as e:
        print(f"  ❌ 场景2错误: {e}")
    
    print("\n🎯 场景3: 系统性能监控")
    try:
        # 分析当前排队系统性能
        service_rate = 60 / queue_data.average_service_time  # 转换为每小时服务率
        arrival_rate = 30  # 假设当前到达率
        
        performance = queue_calculator.analyze_queue_performance(
            arrival_rate=arrival_rate,
            service_rate=service_rate,
            servers=queue_data.active_servers
        )
        
        print(f"  系统监控报告:")
        print(f"    • 当前到达率: {arrival_rate} 顾客/小时")
        print(f"    • 服务率: {service_rate:.1f} 顾客/小时/台")
        print(f"    • 活跃服务台: {queue_data.active_servers} 个")
        print(f"    • 系统状态: {performance['stability_status']}")
        
        if performance['performance_metrics']:
            metrics = performance['performance_metrics']
            print(f"    • 系统利用率: {metrics['utilization']:.1%}")
            print(f"    • 平均等待时间: {metrics['avg_wait_time']:.1f} 分钟")
        
        print(f"    • 系统建议:")
        for rec in performance['recommendations']:
            print(f"      - {rec}")
        
    except Exception as e:
        print(f"  ❌ 场景3错误: {e}")
    
    # 总结
    print_section_header("系统功能总结")
    
    print("\n✅ 已实现的核心功能:")
    print("  🔢 排队论算法:")
    print("    • M/M/1 单服务台模型计算")
    print("    • M/M/c 多服务台模型计算")
    print("    • 顾客位置等待时间预测")
    print("    • 系统性能分析和优化建议")
    
    print("\n  📈 时间序列分析:")
    print("    • ARIMA模型拟合和预测")
    print("    • 季节性分解")
    print("    • 数据平滑处理")
    print("    • 预测准确性评估")
    
    print("\n  ⏰ 等待时间预测:")
    print("    • 基于排队论的精确计算")
    print("    • 历史模式调整")
    print("    • 时段因子调整")
    print("    • 冷启动处理")
    print("    • 置信度评估")
    
    print("\n  📊 人流量预测:")
    print("    • 24小时人流趋势预测")
    print("    • 高峰时段识别")
    print("    • 外部因素调整(天气、节假日)")
    print("    • 经营决策建议")
    print("    • 图表数据生成")
    
    print("\n🎯 应用场景:")
    print("  👤 顾客端: 实时等待时间查询")
    print("  👨‍💼 经理端: 人流预测和经营决策")
    print("  🖥️ 系统端: 性能监控和优化建议")
    
    print("\n📊 技术特点:")
    print("  • 模块化设计，易于扩展")
    print("  • 多算法融合，提高准确性")
    print("  • 冷启动处理，适应新餐厅")
    print("  • 实时调整，持续优化")
    print("  • 置信度评估，透明可靠")
    
    print(f"\n{'='*60}")
    print("  🎉 餐厅排队预测系统演示完成！")
    print(f"{'='*60}")

if __name__ == '__main__':
    test_complete_system() 