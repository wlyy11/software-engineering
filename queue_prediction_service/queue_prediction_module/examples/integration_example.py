"""
餐厅排队预测系统 - 集成示例
演示如何将预测模块集成到现有的餐厅管理系统中
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List
import sys
import os

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from interfaces.prediction_api import PredictionAPI
from interfaces.data_interface import DatabaseInterface, DataAdapter
from models.prediction_models import (
    QueueData, RestaurantConfig, HistoricalData, PredictionContext
)


class MockDatabaseInterface(DatabaseInterface):
    """
    模拟数据库接口实现
    
    在实际项目中，这个类应该由负责数据库的团队实现
    """
    
    def __init__(self):
        """初始化模拟数据库"""
        self.mock_data = self._generate_mock_data()
    
    def get_current_queue_data(self) -> QueueData:
        """获取当前排队数据"""
        return QueueData(
            current_queue_length=12,
            average_service_time=10.0,
            active_servers=3,
            timestamp=datetime.now()
        )
    
    def get_historical_traffic_data(self, start_date: datetime, end_date: datetime) -> HistoricalData:
        """获取历史人流量数据"""
        return HistoricalData(
            hourly_traffic=self.mock_data['hourly_traffic'],
            daily_patterns=self.mock_data['daily_patterns'],
            weekly_patterns=[1.0, 0.9, 1.0, 1.1, 1.2, 1.5, 1.4],
            seasonal_factors={'spring': 1.0, 'summer': 1.2, 'autumn': 1.1, 'winter': 0.9},
            external_factors={'weather_impact': 0.1, 'holiday_impact': 0.3}
        )
    
    def get_restaurant_config(self) -> RestaurantConfig:
        """获取餐厅配置信息"""
        return RestaurantConfig(
            restaurant_type='casual_dining',
            max_capacity=100,
            table_count=20,
            operating_hours=(10, 22),
            peak_hours=[12, 13, 18, 19, 20]
        )
    
    def save_prediction_result(self, prediction_data: Dict[str, Any]) -> bool:
        """保存预测结果"""
        print(f"保存预测结果: {prediction_data.get('type', 'unknown')} - {prediction_data.get('timestamp', 'no_time')}")
        return True
    
    def get_real_time_updates(self) -> List[Dict[str, Any]]:
        """获取实时数据更新"""
        return [
            {
                'type': 'queue_update',
                'queue_length': 15,
                'timestamp': datetime.now(),
                'active_servers': 3
            },
            {
                'type': 'customer_served',
                'service_time': 8.5,
                'timestamp': datetime.now() - timedelta(minutes=2)
            }
        ]
    
    def _generate_mock_data(self) -> Dict[str, Any]:
        """生成模拟历史数据"""
        # 生成过去7天的模拟数据
        mock_data = {
            'hourly_traffic': {},
            'daily_patterns': {
                'monday': [3, 2, 1, 1, 2, 4, 8, 12, 18, 22, 28, 35, 42, 30, 20, 15, 12, 20, 35, 40, 30, 20, 12, 6],
                'tuesday': [2, 1, 1, 1, 2, 3, 6, 10, 15, 20, 25, 32, 38, 28, 18, 12, 10, 18, 32, 38, 28, 18, 10, 5],
                'wednesday': [3, 2, 1, 1, 2, 4, 7, 11, 16, 21, 27, 34, 40, 29, 19, 14, 11, 19, 34, 39, 29, 19, 11, 6],
                'thursday': [4, 3, 2, 1, 3, 5, 9, 14, 20, 25, 32, 40, 48, 35, 25, 18, 15, 25, 42, 48, 35, 25, 15, 8],
                'friday': [5, 4, 2, 2, 4, 6, 12, 18, 25, 30, 38, 48, 55, 40, 30, 22, 18, 30, 50, 60, 45, 30, 18, 10],
                'saturday': [6, 5, 3, 2, 4, 7, 15, 22, 30, 35, 45, 55, 65, 50, 35, 25, 20, 35, 55, 70, 55, 35, 22, 12],
                'sunday': [5, 4, 3, 2, 3, 6, 12, 18, 25, 30, 40, 50, 60, 45, 30, 20, 15, 25, 45, 55, 40, 25, 15, 8]
            }
        }
        
        # 生成具体日期的数据
        base_date = datetime.now() - timedelta(days=7)
        for i in range(7):
            date_str = (base_date + timedelta(days=i)).strftime('%Y-%m-%d')
            day_name = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'][i % 7]
            mock_data['hourly_traffic'][date_str] = mock_data['daily_patterns'][day_name].copy()
        
        return mock_data


class RestaurantPredictionSystem:
    """
    餐厅预测系统集成类
    
    展示如何将预测模块集成到餐厅管理系统中
    """
    
    def __init__(self):
        """初始化预测系统"""
        # 初始化数据接口（实际项目中由其他团队提供）
        self.db_interface = MockDatabaseInterface()
        self.data_adapter = DataAdapter(self.db_interface)
        
        # 初始化预测API
        self.prediction_api = PredictionAPI()
        
        # 系统状态
        self.is_initialized = False
        self.last_prediction_time = None
    
    def initialize_system(self) -> bool:
        """初始化预测系统"""
        try:
            print("正在初始化餐厅预测系统...")
            
            # 获取餐厅配置和历史数据
            restaurant_config = self.db_interface.get_restaurant_config()
            historical_data = self.db_interface.get_historical_traffic_data(
                start_date=datetime.now() - timedelta(days=30),
                end_date=datetime.now()
            )
            
            # 初始化预测API
            success = self.prediction_api.initialize_system(historical_data, restaurant_config)
            
            if success:
                self.is_initialized = True
                print("✅ 预测系统初始化成功")
                return True
            else:
                print("❌ 预测系统初始化失败")
                return False
                
        except Exception as e:
            print(f"❌ 初始化过程中发生错误: {e}")
            return False
    
    def get_customer_wait_time(self, customer_position: int) -> Dict[str, Any]:
        """
        获取顾客等待时间预测
        
        Args:
            customer_position: 顾客在队列中的位置
            
        Returns:
            Dict[str, Any]: 预测结果
        """
        if not self.is_initialized:
            return {'error': '系统未初始化'}
        
        try:
            # 获取当前数据
            queue_data = self.db_interface.get_current_queue_data()
            restaurant_config = self.db_interface.get_restaurant_config()
            
            # 创建预测上下文
            context = PredictionContext(
                current_time=datetime.now(),
                weather_info={'temperature': 25, 'weather_type': 'sunny'},
                is_holiday=False,
                local_events=[],
                special_conditions=[]
            )
            
            # 执行预测
            prediction = self.prediction_api.predict_customer_wait_time(
                queue_data=queue_data,
                customer_position=customer_position,
                restaurant_config=restaurant_config,
                context=context
            )
            
            # 保存预测结果
            self.db_interface.save_prediction_result({
                'type': 'wait_time_prediction',
                'customer_position': customer_position,
                'estimated_wait_time': prediction.estimated_wait_time,
                'confidence_level': prediction.confidence_level,
                'timestamp': datetime.now()
            })
            
            self.last_prediction_time = datetime.now()
            
            return {
                'success': True,
                'estimated_wait_time': prediction.estimated_wait_time,
                'confidence_level': prediction.confidence_level,
                'prediction_range': prediction.prediction_range,
                'message': prediction.message
            }
            
        except Exception as e:
            return {'error': f'预测失败: {e}'}
    
    def get_traffic_forecast(self, hours: int = 24) -> Dict[str, Any]:
        """
        获取人流量预测
        
        Args:
            hours: 预测时长（小时）
            
        Returns:
            Dict[str, Any]: 预测结果
        """
        if not self.is_initialized:
            return {'error': '系统未初始化'}
        
        try:
            # 获取当前数据
            restaurant_config = self.db_interface.get_restaurant_config()
            current_traffic = 25  # 假设当前人流量
            
            # 创建预测上下文
            context = PredictionContext(
                current_time=datetime.now(),
                weather_info={'temperature': 22, 'weather_type': 'cloudy'},
                is_holiday=False,
                local_events=[],
                special_conditions=[]
            )
            
            # 执行预测
            prediction = self.prediction_api.predict_traffic_trends(
                current_traffic=current_traffic,
                restaurant_config=restaurant_config,
                prediction_hours=hours,
                context=context
            )
            
            # 保存预测结果
            self.db_interface.save_prediction_result({
                'type': 'traffic_prediction',
                'prediction_hours': hours,
                'peak_periods': prediction.peak_periods,
                'timestamp': datetime.now()
            })
            
            return {
                'success': True,
                'time_slots': prediction.time_slots,
                'predicted_traffic': prediction.predicted_traffic,
                'peak_periods': prediction.peak_periods,
                'chart_data': prediction.chart_data
            }
            
        except Exception as e:
            return {'error': f'预测失败: {e}'}
    
    def update_with_real_data(self) -> bool:
        """使用实时数据更新预测模型"""
        try:
            # 获取实时更新数据
            updates = self.db_interface.get_real_time_updates()
            
            # 处理更新数据
            actual_data = {
                'actual_wait_times': [],
                'actual_traffic': [],
                'timestamp': datetime.now()
            }
            
            for update in updates:
                if update['type'] == 'customer_served':
                    actual_data['actual_wait_times'].append(update['service_time'])
            
            # 更新预测模型
            success = self.prediction_api.update_models_with_real_data(actual_data)
            
            if success:
                print("✅ 模型更新成功")
            else:
                print("⚠️ 模型更新失败")
            
            return success
            
        except Exception as e:
            print(f"❌ 更新过程中发生错误: {e}")
            return False
    
    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        status = self.prediction_api.get_system_status()
        status.update({
            'integration_status': 'active' if self.is_initialized else 'inactive',
            'last_prediction_time': self.last_prediction_time,
            'database_connection': 'connected'
        })
        return status


def main():
    """主函数 - 演示集成使用"""
    print("餐厅排队预测系统 - 集成示例")
    print("=" * 50)
    
    # 创建预测系统
    system = RestaurantPredictionSystem()
    
    # 初始化系统
    if not system.initialize_system():
        print("系统初始化失败，退出演示")
        return
    
    print("\n1. 顾客等待时间预测演示")
    print("-" * 30)
    
    # 预测不同位置顾客的等待时间
    for position in [1, 5, 10, 15]:
        result = system.get_customer_wait_time(position)
        if result.get('success'):
            print(f"第{position}位顾客: {result['estimated_wait_time']:.1f}分钟 "
                  f"(置信度: {result['confidence_level']:.2f})")
        else:
            print(f"第{position}位顾客预测失败: {result.get('error')}")
    
    print("\n2. 人流量预测演示")
    print("-" * 30)
    
    # 预测未来人流量
    traffic_result = system.get_traffic_forecast(12)  # 预测12小时
    if traffic_result.get('success'):
        print(f"预测时段数: {len(traffic_result['time_slots'])}")
        print("高峰时段:")
        for peak in traffic_result['peak_periods']:
            print(f"  {peak.get('time', 'N/A')}: {peak.get('predicted_customers', 'N/A')} 人")
    else:
        print(f"人流量预测失败: {traffic_result.get('error')}")
    
    print("\n3. 实时数据更新演示")
    print("-" * 30)
    
    # 更新模型
    update_success = system.update_with_real_data()
    print(f"模型更新结果: {'成功' if update_success else '失败'}")
    
    print("\n4. 系统状态查询")
    print("-" * 30)
    
    # 获取系统状态
    status = system.get_system_status()
    print(f"系统状态: {status.get('integration_status', 'unknown')}")
    print(f"最后预测时间: {status.get('last_prediction_time', 'N/A')}")
    print(f"数据库连接: {status.get('database_connection', 'unknown')}")
    
    print("\n" + "=" * 50)
    print("集成演示完成")
    print("\n集成要点:")
    print("1. 其他团队需要实现 DatabaseInterface 接口")
    print("2. 前端可以调用 get_customer_wait_time() 和 get_traffic_forecast()")
    print("3. 系统会自动保存预测结果到数据库")
    print("4. 支持实时数据更新以提升预测精度")


if __name__ == "__main__":
    main() 