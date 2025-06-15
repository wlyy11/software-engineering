#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.algorithms.queue_theory import QueueTheoryCalculator

def test_queue_theory():
    """测试排队论算法实现"""
    
    # 创建计算器实例
    calc = QueueTheoryCalculator()
    
    print('=== 排队论算法测试 ===')
    
    # 测试 M/M/1 模型
    print('\n1. M/M/1 模型测试:')
    try:
        result = calc.calculate_mm1_wait_time(arrival_rate=20, service_rate=25)
        print(f'  到达率: 20 顾客/小时, 服务率: 25 顾客/小时')
        print(f'  平均等待时间: {result["avg_wait_time"]:.2f} 分钟')
        print(f'  系统利用率: {result["utilization"]:.3f}')
        print(f'  平均队列长度: {result["avg_queue_length"]:.2f}')
    except Exception as e:
        print(f'  错误: {e}')
    
    # 测试 M/M/c 模型
    print('\n2. M/M/c 模型测试:')
    try:
        result = calc.calculate_mmc_wait_time(arrival_rate=20, service_rate=10, servers=3)
        print(f'  到达率: 20 顾客/小时, 服务率: 10 顾客/小时, 服务台: 3个')
        print(f'  平均等待时间: {result["avg_wait_time"]:.2f} 分钟')
        print(f'  系统利用率: {result["utilization"]:.3f}')
        print(f'  等待概率: {result["prob_wait"]:.3f}')
    except Exception as e:
        print(f'  错误: {e}')
    
    # 测试顾客位置等待时间
    print('\n3. 顾客位置等待时间测试:')
    try:
        wait_time = calc.calculate_customer_position_wait_time(
            current_queue_length=10, customer_position=5, service_rate=12, servers=2
        )
        print(f'  队列长度: 10, 顾客位置: 5, 服务率: 12 顾客/小时, 服务台: 2个')
        print(f'  预计等待时间: {wait_time:.2f} 分钟')
    except Exception as e:
        print(f'  错误: {e}')
    
    # 测试服务率估算
    print('\n4. 服务率估算测试:')
    try:
        historical_times = [3.5, 4.2, 2.8, 5.1, 3.9, 4.5, 3.2]  # 分钟
        service_rate = calc.estimate_service_rate(historical_times)
        print(f'  历史服务时间: {historical_times}')
        print(f'  估算服务率: {service_rate:.2f} 顾客/小时')
    except Exception as e:
        print(f'  错误: {e}')
    
    # 测试最优服务台数量
    print('\n5. 最优服务台数量测试:')
    try:
        optimal_servers = calc.calculate_optimal_servers(
            arrival_rate=30, service_rate=12, target_wait_time=5.0
        )
        print(f'  到达率: 30 顾客/小时, 服务率: 12 顾客/小时, 目标等待时间: 5分钟')
        print(f'  建议服务台数量: {optimal_servers}')
    except Exception as e:
        print(f'  错误: {e}')
    
    # 测试性能分析
    print('\n6. 性能分析测试:')
    try:
        analysis = calc.analyze_queue_performance(
            arrival_rate=25, service_rate=10, servers=3
        )
        print(f'  到达率: 25 顾客/小时, 服务率: 10 顾客/小时, 服务台: 3个')
        print(f'  稳定性状态: {analysis["stability_status"]}')
        if analysis["performance_metrics"]:
            metrics = analysis["performance_metrics"]
            print(f'  平均等待时间: {metrics["avg_wait_time"]:.2f} 分钟')
            print(f'  系统利用率: {metrics["utilization"]:.3f}')
        print(f'  优化建议: {analysis["recommendations"]}')
    except Exception as e:
        print(f'  错误: {e}')
    
    print('\n=== 测试完成! ===')

if __name__ == '__main__':
    test_queue_theory() 