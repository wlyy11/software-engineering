"""
餐厅排队预测系统 - 排队论算法模块
实现各种排队论模型用于等待时间计算
"""

import math
from typing import Dict, Any, Optional, Tuple
from scipy import special
import numpy as np


class QueueTheoryError(Exception):
    """排队论计算异常"""
    pass


class QueueTheoryCalculator:
    """
    排队论计算器
    
    实现多种排队模型：
    1. M/M/1 - 单服务台泊松到达指数服务
    2. M/M/c - 多服务台泊松到达指数服务  
    3. M/G/1 - 单服务台泊松到达一般服务
    """
    
    def __init__(self):
        """初始化排队论计算器"""
        self.stability_threshold = 0.95  # 系统稳定性阈值
    
    def calculate_mm1_wait_time(self, arrival_rate: float, service_rate: float) -> Dict[str, float]:
        """
        计算M/M/1排队模型的等待时间
        
        Args:
            arrival_rate: 到达率 (顾客/小时)
            service_rate: 服务率 (顾客/小时)
            
        Returns:
            Dict[str, float]: 包含各种等待时间指标的字典
                - avg_wait_time: 平均等待时间(分钟)
                - avg_system_time: 平均系统时间(分钟)
                - utilization: 系统利用率
                - avg_queue_length: 平均队列长度
                
        Raises:
            QueueTheoryError: 当系统不稳定时抛出
        """
        if arrival_rate <= 0 or service_rate <= 0:
            raise QueueTheoryError("到达率和服务率必须大于0")
        
        # 计算系统利用率
        rho = arrival_rate / service_rate
        
        # 检查系统稳定性
        if rho >= self.stability_threshold:
            raise QueueTheoryError(f"系统不稳定: 利用率 {rho:.3f} >= {self.stability_threshold}")
        
        # M/M/1模型公式计算
        # 平均等待时间 (分钟)
        avg_wait_time = (rho / (service_rate * (1 - rho))) * 60
        
        # 平均系统时间 (分钟) = 等待时间 + 服务时间
        avg_service_time = (1 / service_rate) * 60  # 转换为分钟
        avg_system_time = avg_wait_time + avg_service_time
        
        # 平均队列长度 (不包括正在服务的顾客)
        avg_queue_length = (rho ** 2) / (1 - rho)
        
        return {
            'avg_wait_time': avg_wait_time,
            'avg_system_time': avg_system_time,
            'utilization': rho,
            'avg_queue_length': avg_queue_length
        }
    
    def calculate_mmc_wait_time(self, arrival_rate: float, service_rate: float, 
                              servers: int) -> Dict[str, float]:
        """
        计算M/M/c排队模型的等待时间
        
        Args:
            arrival_rate: 到达率 (顾客/小时)
            service_rate: 每个服务台的服务率 (顾客/小时)
            servers: 服务台数量
            
        Returns:
            Dict[str, float]: 包含各种等待时间指标的字典
                - avg_wait_time: 平均等待时间(分钟)
                - avg_system_time: 平均系统时间(分钟)
                - utilization: 系统利用率
                - avg_queue_length: 平均队列长度
                - prob_wait: 需要等待的概率
                
        Raises:
            QueueTheoryError: 当系统不稳定或参数无效时抛出
        """
        if not self._validate_stability(arrival_rate, service_rate, servers):
            raise QueueTheoryError("系统参数无效或不稳定")
        
        # 计算系统负载强度
        rho = arrival_rate / service_rate
        
        # 计算系统利用率
        utilization = rho / servers
        
        # 计算等待概率 (Erlang C)
        prob_wait = self._calculate_erlang_c(rho, servers)
        
        # 计算平均等待时间 (分钟)
        if prob_wait > 0:
            avg_wait_time = (prob_wait / (servers * service_rate - arrival_rate)) * 60
        else:
            avg_wait_time = 0.0
        
        # 计算平均服务时间 (分钟)
        avg_service_time = (1 / service_rate) * 60
        
        # 计算平均系统时间 (分钟)
        avg_system_time = avg_wait_time + avg_service_time
        
        # 计算平均队列长度 (不包括正在服务的顾客)
        avg_queue_length = (arrival_rate * avg_wait_time) / 60  # 转换回小时单位计算
        
        return {
            'avg_wait_time': avg_wait_time,
            'avg_system_time': avg_system_time,
            'utilization': utilization,
            'avg_queue_length': avg_queue_length,
            'prob_wait': prob_wait
        }
    
    def calculate_customer_position_wait_time(self, current_queue_length: int, 
                                            customer_position: int,
                                            service_rate: float, 
                                            servers: int) -> float:
        """
        计算特定位置顾客的等待时间
        
        Args:
            current_queue_length: 当前排队人数
            customer_position: 顾客在队列中的位置 (1表示队首)
            service_rate: 每个服务台的服务率 (顾客/小时)
            servers: 服务台数量
            
        Returns:
            float: 该顾客的预计等待时间(分钟)
        """
        if customer_position <= 0 or service_rate <= 0 or servers <= 0:
            raise QueueTheoryError("参数必须大于0")
        
        if customer_position > current_queue_length:
            raise QueueTheoryError("顾客位置不能超过队列长度")
        
        # 计算平均服务时间 (分钟)
        avg_service_time = (1 / service_rate) * 60
        
        # 如果有多个服务台，考虑并行服务
        if servers >= customer_position:
            # 如果服务台数量 >= 顾客前面的人数，顾客可能立即得到服务
            return 0.0
        else:
            # 计算需要等待的人数 (顾客前面的人数 - 正在服务的人数)
            people_ahead = customer_position - 1
            people_waiting = max(0, people_ahead - servers)
            
            # 等待时间 = (等待人数 / 服务台数量) * 平均服务时间
            wait_time = (people_waiting / servers) * avg_service_time
            
            return wait_time
    
    def _calculate_erlang_c(self, rho: float, servers: int) -> float:
        """
        计算Erlang C公式 (等待概率)
        
        Args:
            rho: 系统负载强度
            servers: 服务台数量
            
        Returns:
            float: 等待概率
        """
        if servers <= 0:
            raise QueueTheoryError("服务台数量必须大于0")
        
        # 计算分子: (rho^c / c!) * (c / (c - rho))
        numerator = (rho ** servers) / math.factorial(servers)
        numerator *= servers / (servers - rho)
        
        # 计算分母: sum(rho^k / k!) for k=0 to c-1 + (rho^c / c!) * (c / (c - rho))
        denominator = 0
        for k in range(servers):
            denominator += (rho ** k) / math.factorial(k)
        denominator += numerator
        
        # Erlang C 公式
        erlang_c = numerator / denominator
        
        return min(erlang_c, 1.0)  # 确保概率不超过1
    
    def _validate_stability(self, arrival_rate: float, service_rate: float, servers: int) -> bool:
        """
        验证排队系统的稳定性
        
        Args:
            arrival_rate: 到达率
            service_rate: 服务率
            servers: 服务台数量
            
        Returns:
            bool: 系统是否稳定
        """
        if arrival_rate <= 0 or service_rate <= 0 or servers <= 0:
            return False
        
        # 总服务能力
        total_service_rate = service_rate * servers
        
        # 系统稳定条件: 到达率 < 总服务率
        utilization = arrival_rate / total_service_rate
        
        return utilization < self.stability_threshold
    
    def estimate_service_rate(self, historical_service_times: list) -> float:
        """
        基于历史服务时间估算服务率
        
        Args:
            historical_service_times: 历史服务时间列表(分钟)
            
        Returns:
            float: 估算的服务率 (顾客/小时)
        """
        if not historical_service_times:
            raise QueueTheoryError("历史服务时间数据不能为空")
        
        # 过滤无效数据
        valid_times = [t for t in historical_service_times if t > 0]
        if not valid_times:
            raise QueueTheoryError("没有有效的服务时间数据")
        
        # 计算平均服务时间 (分钟)
        avg_service_time = sum(valid_times) / len(valid_times)
        
        # 转换为服务率 (顾客/小时)
        service_rate = 60 / avg_service_time
        
        return service_rate
    
    def estimate_arrival_rate(self, historical_arrivals: list, time_window: int) -> float:
        """
        基于历史到达数据估算到达率
        
        Args:
            historical_arrivals: 历史到达时间列表
            time_window: 时间窗口(小时)
            
        Returns:
            float: 估算的到达率 (顾客/小时)
        """
        if not historical_arrivals or time_window <= 0:
            raise QueueTheoryError("历史到达数据不能为空且时间窗口必须大于0")
        
        # 计算到达率 (顾客数 / 时间窗口)
        arrival_rate = len(historical_arrivals) / time_window
        
        return arrival_rate
    
    def calculate_optimal_servers(self, arrival_rate: float, service_rate: float, 
                                target_wait_time: float) -> int:
        """
        计算达到目标等待时间所需的最优服务台数量
        
        Args:
            arrival_rate: 到达率
            service_rate: 单个服务台服务率
            target_wait_time: 目标等待时间(分钟)
            
        Returns:
            int: 建议的服务台数量
        """
        if arrival_rate <= 0 or service_rate <= 0 or target_wait_time < 0:
            raise QueueTheoryError("参数必须为正数")
        
        # 最少需要的服务台数量 (保证系统稳定)
        min_servers = math.ceil(arrival_rate / service_rate) + 1
        
        # 从最少服务台数量开始尝试
        for servers in range(min_servers, min_servers + 20):  # 限制搜索范围
            try:
                result = self.calculate_mmc_wait_time(arrival_rate, service_rate, servers)
                if result['avg_wait_time'] <= target_wait_time:
                    return servers
            except QueueTheoryError:
                continue
        
        # 如果找不到合适的服务台数量，返回一个较大的值
        return min_servers + 10
    
    def analyze_queue_performance(self, arrival_rate: float, service_rate: float, 
                                servers: int) -> Dict[str, Any]:
        """
        全面分析排队系统性能
        
        Args:
            arrival_rate: 到达率
            service_rate: 服务率
            servers: 服务台数量
            
        Returns:
            Dict[str, Any]: 性能分析结果
                - performance_metrics: 性能指标
                - recommendations: 优化建议
                - stability_status: 稳定性状态
        """
        result = {
            'performance_metrics': {},
            'recommendations': [],
            'stability_status': 'unknown'
        }
        
        try:
            # 检查系统稳定性
            is_stable = self._validate_stability(arrival_rate, service_rate, servers)
            result['stability_status'] = 'stable' if is_stable else 'unstable'
            
            if not is_stable:
                result['recommendations'].append("系统不稳定，需要增加服务台数量或提高服务效率")
                return result
            
            # 计算性能指标
            if servers == 1:
                metrics = self.calculate_mm1_wait_time(arrival_rate, service_rate)
            else:
                metrics = self.calculate_mmc_wait_time(arrival_rate, service_rate, servers)
            
            result['performance_metrics'] = metrics
            
            # 生成优化建议
            utilization = metrics['utilization']
            avg_wait_time = metrics['avg_wait_time']
            
            if utilization > 0.8:
                result['recommendations'].append("系统利用率过高，建议增加服务台或提高服务效率")
            elif utilization < 0.3:
                result['recommendations'].append("系统利用率较低，可以考虑减少服务台数量")
            
            if avg_wait_time > 10:
                result['recommendations'].append("平均等待时间过长，建议优化服务流程")
            elif avg_wait_time < 2:
                result['recommendations'].append("等待时间很短，服务效率良好")
            
            # 计算建议的服务台数量
            optimal_servers = self.calculate_optimal_servers(arrival_rate, service_rate, 5.0)  # 目标5分钟
            if optimal_servers != servers:
                result['recommendations'].append(f"建议使用 {optimal_servers} 个服务台以达到更好的性能")
            
        except QueueTheoryError as e:
            result['recommendations'].append(f"分析出错: {str(e)}")
        
        return result 