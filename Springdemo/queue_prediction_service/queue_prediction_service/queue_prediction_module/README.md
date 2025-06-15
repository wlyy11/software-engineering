# 餐厅排队预测系统

## 项目概述

这是一个专门用于餐厅排队预测的算法模块，提供两个核心功能：

1. **顾客等待时间预测** - 告诉顾客大约还要多久能排到
2. **人流量趋势预测** - 向经理预测后续的人流高峰时刻并生成预测图表

## 项目结构

```
queue_prediction_module/
├── src/                          # 源代码
│   ├── models/                   # 数据模型定义
│   │   └── prediction_models.py  # 预测相关数据结构
│   ├── predictors/               # 预测器
│   │   ├── base_predictor.py     # 预测器基类
│   │   ├── wait_time_predictor.py # 等待时间预测器
│   │   └── traffic_predictor.py   # 人流量预测器
│   ├── algorithms/               # 核心算法
│   │   ├── queue_theory.py       # 排队论算法
│   │   └── time_series_analysis.py # 时间序列分析
│   ├── interfaces/               # 对外接口
│   │   ├── prediction_api.py     # 预测API接口
│   │   └── data_interface.py     # 数据输入接口
│   └── utils/                    # 工具类
│       └── data_processor.py     # 数据处理工具
├── tests/                        # 测试文件
├── examples/                     # 使用示例
├── requirements.txt              # 依赖包
└── README.md                     # 项目说明
```

## 核心功能

### 1. 等待时间预测 (给顾客)

**输入数据：**
- 当前排队人数
- 顾客在队列中的位置
- 餐厅配置信息（服务台数量、餐厅类型等）

**输出结果：**
- 预计等待时间（分钟）
- 预测置信度
- 时间范围（最小-最大）
- 友好的提示信息

**使用的算法：**
- 排队论模型 (M/M/c)
- 历史模式匹配
- 冷启动处理

### 2. 人流量预测 (给经理)

**输入数据：**
- 历史人流量数据
- 当前时间和人流状况
- 外部因素（天气、节假日等）

**输出结果：**
- 未来24小时人流量预测曲线
- 高峰时段识别
- 置信区间
- 可视化图表数据

**使用的算法：**
- ARIMA时间序列分析
- 机器学习回归模型
- 季节性分解
- 模式识别

## 技术特点

### 算法优势
- **实时性强** - 排队论算法计算速度快，适合实时预测
- **准确性高** - 多模型集成，提高预测精度
- **鲁棒性好** - 处理冷启动和数据不足问题
- **可扩展性** - 模块化设计，易于添加新算法

### 冷启动解决方案
- **默认模式** - 基于餐厅类型的行业标准
- **渐进学习** - 随数据积累逐步提升精度
- **外部数据** - 结合天气、节假日等信息
- **置信度管理** - 透明的预测可靠性指示

## 接口设计

### 数据输入接口 (供其他团队实现)

```python
class DatabaseInterface:
    def get_current_queue_data() -> QueueData
    def get_historical_traffic_data(start_date, end_date) -> HistoricalData
    def get_restaurant_config() -> RestaurantConfig
```

### 预测输出接口 (供前端调用)

```python
class PredictionAPI:
    def predict_customer_wait_time(queue_data, customer_position) -> WaitTimePrediction
    def predict_traffic_trends(current_traffic, prediction_hours) -> TrafficPrediction
```

## 安装和使用

### 环境要求
- Python 3.8+
- 依赖包见 requirements.txt

### 安装依赖
```bash
python -m pip install -r requirements.txt
```

### 基本使用示例

```python
from src.interfaces.prediction_api import PredictionAPI
from src.models.prediction_models import QueueData, RestaurantConfig

# 初始化预测API
api = PredictionAPI()

# 预测顾客等待时间
queue_data = QueueData(current_queue_length=15, average_service_time=8.0, active_servers=3)
config = RestaurantConfig(restaurant_type='fast_food', max_capacity=100, table_count=20)

wait_prediction = api.predict_customer_wait_time(queue_data, customer_position=10, restaurant_config=config)
print(f"预计等待时间: {wait_prediction.estimated_wait_time} 分钟")

# 预测人流量趋势
traffic_prediction = api.predict_traffic_trends(current_traffic=25, restaurant_config=config)
print(f"高峰时段: {traffic_prediction.peak_periods}")
```

## 开发计划

### 已完成
- ✅ 项目架构设计
- ✅ 接口定义
- ✅ 数据模型设计
- ✅ 函数框架搭建

### 待实现
- ⏳ 排队论算法实现
- ⏳ 时间序列分析实现
- ⏳ 预测器逻辑实现
- ⏳ 数据处理工具实现
- ⏳ 测试用例编写
- ⏳ 使用示例完善

## 贡献指南

1. 本模块专注于预测算法，不涉及数据库和前端
2. 所有函数都有详细的类型注解和文档字符串
3. 遵循模块化设计，便于其他团队集成
4. 提供清晰的接口规范，方便协作开发

## 联系方式

如有问题或建议，请联系预测算法团队。 