 # 顾客排队时间预测系统说明文档

## 项目概述

本系统为顾客提供精确的排队时间预测服务，基于队列理论和实时数据分析，帮助顾客合理安排用餐时间，提升用餐体验。

## 系统架构

### 整体架构
```
顾客端请求 → Spring Boot API → Flask预测服务 → 队列算法计算 → 返回等待时间
```

### 技术栈
- **后端框架**: Spring Boot 3.x + JPA
- **预测服务**: Flask + Python 3.12
- **算法**: 队列理论 (M/M/c排队模型)
- **数据库**: MySQL 8.0

## 新增模块结构

### 1. Spring Boot后端模块

#### QueuePredictionController (队列预测控制器)
**文件路径**: `Springdemo/src/main/java/com/example/springdemo/interfac/QueuePredictionController.java`

**主要功能**:
- 个人等待时间预测
- 队列位置计算
- 预约状态管理
- 实时队列信息获取

**核心方法**:
```java
@GetMapping("/queue-prediction/{restaurantId}")
public ResponseEntity<QueuePredictionResponse> predictQueueTime(
    @PathVariable int restaurantId
)
```

**实现特点**:
- 基于M/M/c排队模型的精确计算
- 考虑服务台数量和服务效率
- 动态调整预测参数
- 提供置信区间评估

### 2. Flask预测服务模块

#### 等待时间预测器
**文件路径**: `queue_prediction_service/queue_prediction_module/src/predictors/wait_time_predictor.py`

**核心算法**:
```python
class WaitTimePredictor(BasePredictor):
    def predict(self, input_data: Dict, context: PredictionContext) -> WaitTimePrediction:
        # 队列理论算法
        # M/M/c排队模型
        # 动态参数调整
```

**算法实现**:
- **基础计算**: `等待时间 = 队列长度 / 服务台数量 * 平均服务时间`
- **置信度评估**: 基于历史数据方差计算
- **动态调整**: 考虑餐厅类型、时段、客流密度等因素

## 核心功能实现

### 1. 队列理论算法

#### M/M/c排队模型
**实现位置**: `WaitTimePredictor.calculate_wait_time()`

```python
def calculate_wait_time(self, queue_length, service_rate, num_servers):
    # 基础等待时间计算
    if queue_length == 0:
        return 0.0
    
    # 平均服务时间 (分钟)
    avg_service_time = 1.0 / service_rate
    
    # 考虑多服务台的并行处理
    effective_service_rate = service_rate * num_servers
    
    # 队列等待时间
    wait_time = queue_length / effective_service_rate
    
    return wait_time
```

#### 动态参数调整
```python
def adjust_parameters(self, restaurant_type, current_hour, queue_density):
    # 根据餐厅类型调整服务效率
    if restaurant_type == "快餐":
        service_multiplier = 1.2
    elif restaurant_type == "正餐":
        service_multiplier = 0.8
    else:
        service_multiplier = 1.0
    
    # 根据时段调整
    if 11 <= current_hour <= 13 or 17 <= current_hour <= 19:
        # 高峰期服务效率略降
        service_multiplier *= 0.9
    
    return service_multiplier
```

### 2. 置信度计算

#### 置信区间评估
```python
def calculate_confidence(self, predicted_time, historical_variance):
    # 基于历史数据方差计算置信度
    if historical_variance == 0:
        return 0.8  # 默认置信度
    
    # 标准差
    std_dev = math.sqrt(historical_variance)
    
    # 置信区间 (±1个标准差约68%置信度)
    confidence = max(0.5, min(0.95, 1.0 - (std_dev / predicted_time)))
    
    return confidence
```

## 使用方法

### 1. API调用示例

#### 获取排队时间预测
```bash
curl -X GET "http://localhost:8080/api/test/queue-prediction/4"
```

**响应示例**:
```json
{
  "estimatedWaitTime": 2.0,
  "confidence": 0.76,
  "message": "很快就能得到服务",
  "predictionRange": [1.76, 2.24],
  "customerPosition": 3,
  "timestamp": "2025-06-13T23:51:37.834650"
}
```

### 2. 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `estimatedWaitTime` | double | 预估等待时间(分钟) |
| `confidence` | double | 预测置信度(0-1) |
| `message` | string | 友好提示信息 |
| `predictionRange` | array | 等待时间范围[最小值, 最大值] |
| `customerPosition` | int | 当前队列位置 |
| `timestamp` | string | 预测时间戳 |

### 3. 消息提示规则

```java
if (waitTime <= 1.0) {
    message = "很快就能得到服务";
} else if (waitTime <= 3.0) {
    message = "稍等片刻即可";
} else if (waitTime <= 5.0) {
    message = "预计需要等待几分钟";
} else {
    message = "当前人较多，建议稍后再来";
}
```

## 数据库设计

### 相关表结构

#### tb_appointment (预约表)
```sql
CREATE TABLE tb_appointment (
    appointment_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    restaurant_id INT,
    appointment_status ENUM('WAITING', 'CONFIRMED', 'CANCELLED'),
    appointment_time DATETIME,
    estimated_wait_time DOUBLE,  -- 预估等待时间
    actual_wait_time DOUBLE,     -- 实际等待时间
    queue_position INT,          -- 队列位置
    FOREIGN KEY (user_id) REFERENCES tb_user(user_id),
    FOREIGN KEY (restaurant_id) REFERENCES tb_restaurant(restaurant_id)
);
```

#### tb_restaurant (餐厅表)
```sql
CREATE TABLE tb_restaurant (
    restaurant_id INT PRIMARY KEY,
    restaurant_name VARCHAR(100),
    restaurant_max_capacity INT,
    service_counter_count INT,   -- 服务台数量
    avg_service_time DOUBLE,     -- 平均服务时间(分钟)
    restaurant_type VARCHAR(50), -- 餐厅类型(快餐/正餐)
    restaurant_local VARCHAR(200),
    restaurant_manager_id INT
);
```

## 扩展功能

### 已实现功能
-  M/M/c排队模型算法
-  动态参数调整
-  置信度计算
-  友好消息提示
-  多餐厅支持
-  实时状态更新

