# 队列预测系统详细说明文档

## 项目概述

本项目在原有软件工程基础上，新增了完整的**队列预测系统**，实现了餐厅人流量预测、等待时间估算和可视化图表生成功能。系统采用微服务架构，结合Spring Boot后端和Flask预测服务，提供准确的队列预测和直观的数据展示。

## 系统架构

### 整体架构图
```
┌─────────────────┐    HTTP API    ┌─────────────────┐
│   Spring Boot   │ ──────────────→ │  Flask Service  │
│   (端口 8080)   │ ←────────────── │   (端口 5000)   │
└─────────────────┘                └─────────────────┘
         │                                   │
         ▼                                   ▼
┌─────────────────┐                ┌─────────────────┐
│   MySQL 数据库  │                │  图表生成模块   │
│  (人流数据存储) │                │  (matplotlib)   │
└─────────────────┘                └─────────────────┘
```

### 技术栈
- **后端框架**: Spring Boot 3.x + JPA + Hibernate
- **数据库**: MySQL 8.0
- **预测服务**: Flask + Python 3.12
- **算法库**: NumPy, SciPy, matplotlib
- **图表生成**: matplotlib (300 DPI高质量输出)
- **API通信**: RESTful API + JSON

## 新增模块结构

### 1. Spring Boot后端模块

#### 1.1 TestController (测试控制器)
**文件路径**: `Springdemo/src/main/java/com/example/springdemo/interfac/TestController.java`

**主要功能**:
- 队列预测API接口
- 人流高峰预测
- 图表生成调用
- 数据库时间解析优化

**核心方法**:
```java
@GetMapping("/peak-prediction/{restaurantId}/{hoursAhead}")
public ResponseEntity<Map<String, Object>> predictPeakHours(
    @PathVariable int restaurantId, 
    @PathVariable double hoursAhead
)
```

**实现特点**:
- 支持0.5小时（30分钟）短期预测
- 5分钟间隔预测（6个预测点）
- 自动调整时间到5分钟倍数
- 集成历史数据分析

#### 1.2 QueuePredictionController (队列预测控制器)
**文件路径**: `Springdemo/src/main/java/com/example/springdemo/interfac/QueuePredictionController.java`

**主要功能**:
- 个人等待时间预测
- 队列位置计算
- 预约状态管理

#### 1.3 数据模型优化

**QueuePredictionRequest/Response**:
```java
public class QueuePredictionResponse {
    private double estimatedWaitTime;
    private double confidence;
    private String message;
    private List<Double> predictionRange;
    private int customerPosition;
    private Map<String, Object> chartData;
}
```

### 2. Flask预测服务模块

#### 2.1 主服务文件
**文件路径**: `queue_prediction_service/app.py`

**核心API端点**:
```python
@app.route('/api/predict/wait-time', methods=['POST'])
def predict_wait_time():
    # 等待时间预测

@app.route('/api/predict/traffic', methods=['POST'])
def predict_traffic():
    # 人流量预测

@app.route('/api/chart/<filename>')
def get_chart(filename):
    # 图表文件访问
```

**图表生成功能**:
- 300 DPI高质量PNG输出
- 蓝色历史数据 + 红色预测数据
- 自动时间轴标签（5分钟倍数）
- 整数纵坐标（人数）

#### 2.2 预测算法模块

**文件路径**: `queue_prediction_service/queue_prediction_module/src/predictors/`

##### 2.2.1 TrafficPredictor (人流预测器)
```python
class TrafficPredictor(BasePredictor):
    def predict(self, input_data: Dict, context: PredictionContext) -> TrafficPrediction:
        # 时间序列分析
        # 冷启动处理
        # 动态调整算法
```

**算法特点**:
- **冷启动预测**: 基于时间模式的初始预测
- **动态调整**: 70%实际数据 + 30%历史模式
- **时间衰减**: 深夜时段80%-100%衰减因子
- **随机变化**: 15%的自然波动模拟

##### 2.2.2 WaitTimePredictor (等待时间预测器)
```python
class WaitTimePredictor(BasePredictor):
    def predict(self, input_data: Dict, context: PredictionContext) -> WaitTimePrediction:
        # 队列理论算法
        # M/M/c排队模型
```

**算法实现**:
- **基础计算**: `等待时间 = 队列长度 / 服务台数量 * 平均服务时间`
- **置信度评估**: 基于历史数据方差
- **动态调整**: 考虑餐厅类型、时段、天气等因素

#### 2.3 数据模型

**文件路径**: `queue_prediction_service/queue_prediction_module/src/models/prediction_models.py`

```python
@dataclass
class TrafficPrediction:
    time_slots: List[str]
    predicted_traffic: List[int]
    peak_periods: List[Dict]
    chart_data: Dict
    confidence_level: float

@dataclass
class QueueData:
    current_queue_length: int
    average_service_time: float
    active_servers: int
    timestamp: datetime
```

## 核心功能实现

### 1. 时间处理优化

#### 1.1 数据库时间解析
**实现位置**: `TestController.parseRecordTimeToISO()`

```java
private String parseRecordTimeToISO(String recordTime) {
    // 解析格式: "6_12_12_35" -> "2025-06-12T12:35"
    String[] parts = recordTime.split("_");
    int month = Integer.parseInt(parts[0]);
    int day = Integer.parseInt(parts[1]);
    int hour = Integer.parseInt(parts[2]);
    int minute = Integer.parseInt(parts[3]);
    
    // 调整到5分钟倍数
    int adjustedMinute = (minute / 5) * 5;
    LocalDateTime adjustedDateTime = LocalDateTime.of(year, month, day, hour, adjustedMinute);
    
    return adjustedDateTime.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
}
```

#### 1.2 预测时间生成
**实现位置**: `TrafficPredictor._generate_time_slots_minutes()`

```python
def _generate_time_slots_minutes(self, start_time: datetime, intervals: int, interval_minutes: int):
    # 计算下一个5分钟时刻
    current_minute = start_time.minute
    next_5min_minute = ((current_minute // 5) + 1) * 5
    
    if next_5min_minute >= 60:
        next_start_time = start_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    else:
        next_start_time = start_time.replace(minute=next_5min_minute, second=0, microsecond=0)
    
    time_slots = []
    for i in range(intervals):
        slot_time = next_start_time + timedelta(minutes=i * interval_minutes)
        time_slots.append(slot_time.strftime("%H:%M"))
    
    return time_slots
```

### 2. 图表生成系统

#### 2.1 图表配置
**实现位置**: `app.py generate_traffic_chart()`

```python
def generate_traffic_chart(request_data, prediction, context):
    # 创建14x8英寸图表
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # 历史数据（蓝色）
    ax.plot(past_times, past_counts, 'b-', linewidth=2, marker='o', 
           markersize=6, label='Historical Data (Past 15 Minutes)', alpha=0.8)
    
    # 预测数据（红色）+ 连接线
    if past_times and past_counts:
        connection_times = [past_times[-1], future_times[0]]
        connection_counts = [past_counts[-1], future_counts[0]]
        ax.plot(connection_times, connection_counts, 'r-', linewidth=2, alpha=0.8)
    
    ax.plot(future_times, future_counts, 'r-', linewidth=2, marker='s', 
           markersize=6, label='Predicted Traffic', alpha=0.8)
    
    # 强制整数Y轴
    from matplotlib.ticker import MaxNLocator
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    
    # 手动设置X轴时间标签
    all_times = past_times + future_times
    ax.set_xticks(all_times)
    ax.set_xticklabels([t.strftime('%H:%M') for t in all_times], rotation=45)
```

#### 2.2 图表特性
- **分辨率**: 300 DPI高质量输出
- **尺寸**: 14x8英寸，适合展示
- **颜色方案**: 蓝色历史 + 红色预测
- **标题格式**: "Traffic prediction for id: {restaurant_id}"
- **文件命名**: `traffic_prediction_{id}_{timestamp}.png`

### 3. 预测算法详解

#### 3.1 冷启动预测算法
```python
def _cold_start_prediction(self, current_time, current_traffic, hours_ahead):
    # 基于时间模式的预测
    hour = current_time.hour
    
    if 6 <= hour < 11:      # 早餐时段
        base_pattern = [30, 45, 60, 50, 35, 25]
    elif 11 <= hour < 14:   # 午餐时段  
        base_pattern = [40, 60, 80, 70, 50, 35]
    elif 17 <= hour < 20:   # 晚餐时段
        base_pattern = [35, 55, 75, 65, 45, 30]
    else:                   # 其他时段
        base_pattern = [10, 15, 20, 15, 10, 8]
    
    # 动态调整
    if current_traffic > 0:
        adjustment_ratio = min(current_traffic / pattern_avg, 2.0)
        adjusted_pattern = [int(p * adjustment_ratio) for p in base_pattern]
    
    return adjusted_pattern
```

#### 3.2 数据扩展算法
```python
def _expand_prediction_to_intervals(self, base_predictions, target_intervals):
    if len(base_predictions) == target_intervals:
        return base_predictions
    
    expanded = []
    for i in range(target_intervals):
        base_index = i * len(base_predictions) / target_intervals
        base_value = base_predictions[int(base_index)]
        
        # 添加变化
        variation = random.uniform(-0.15, 0.15) * base_value
        final_value = max(1, int(base_value + variation))
        expanded.append(final_value)
    
    return expanded
```

### 3. 冷启动预测算法

#### 算法实现
**实现位置**: `TrafficPredictor._cold_start_prediction()`

```python
def _cold_start_prediction(self, current_time, current_traffic, hours_ahead):
    # 基于时间模式的预测
    hour = current_time.hour
    
    if 6 <= hour < 11:      # 早餐时段
        base_pattern = [30, 45, 60, 50, 35, 25]
    elif 11 <= hour < 14:   # 午餐时段  
        base_pattern = [40, 60, 80, 70, 50, 35]
    elif 17 <= hour < 20:   # 晚餐时段
        base_pattern = [35, 55, 75, 65, 45, 30]
    else:                   # 其他时段
        base_pattern = [10, 15, 20, 15, 10, 8]
    
    # 动态调整
    if current_traffic > 0:
        pattern_avg = sum(base_pattern) / len(base_pattern)
        adjustment_ratio = min(current_traffic / pattern_avg, 2.0)
        adjusted_pattern = [int(p * adjustment_ratio) for p in base_pattern]
    
    # 深夜衰减
    if hour >= 22 or hour < 6:
        decay_factor = random.uniform(0.8, 1.0)
        adjusted_pattern = [int(p * decay_factor) for p in adjusted_pattern]
    
    return adjusted_pattern
```

**算法特点**:
- **时段识别**: 自动识别早餐、午餐、晚餐、其他时段
- **基础模式**: 每个时段有预定义的人流模式
- **动态调整**: 根据当前实际人流调整预测基准
- **深夜处理**: 深夜时段应用衰减因子
- **上限保护**: 调整比例最大不超过2倍

## 使用方法

### 1. 环境配置

#### 1.1 Python环境
```bash
cd queue_prediction_service
pip install -r requirements.txt
```

**依赖包**:
```
Flask==2.1.2
Flask-CORS==4.0.0
numpy==1.24.3
matplotlib==3.7.1
scipy==1.10.1
requests==2.32.3
```

#### 1.2 Java环境
```bash
cd Springdemo
mvn clean install
```

### 2. 服务启动

#### 2.1 启动Flask预测服务
```bash
cd queue_prediction_service
python -m flask run --host=0.0.0.0 --port=5000
```

#### 2.2 启动Spring Boot服务
```bash
cd Springdemo
mvn spring-boot:run
```

### 3. API使用示例

#### 3.1 人流预测API
```bash
curl -X GET "http://localhost:8080/api/test/peak-prediction/4/0.5"
```

**响应示例**:
```json
{
  "summary": "餐厅 第一饭堂 当前有 10 人，未来预测： 12:40→19人, 12:45→16人, 12:50→19人",
  "timeSlots": ["12:40", "12:45", "12:50", "12:55", "13:00", "13:05"],
  "predictedTraffic": [19, 16, 19, 18, 20, 18],
  "chartUrl": "http://localhost:5000/api/chart/traffic_prediction_4_20250614_000345.png",
  "chartData": {
    "confidence_bands": {
      "lower": [15, 12, 15, 14, 16, 14],
      "upper": [22, 19, 22, 21, 24, 21]
    },
    "x_axis": {"data": ["12:40", "12:45", "12:50", "12:55", "13:00", "13:05"]},
    "y_axis": {"data": [19, 16, 19, 18, 20, 18]}
  }
}
```

#### 3.2 等待时间预测API
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

### 4. 图表访问
```bash
curl -X GET "http://localhost:5000/api/chart/traffic_prediction_4_20250614_000345.png" --output chart.png
```

## 数据库设计

### 相关表结构

#### tb_record (人流记录表)
```sql
CREATE TABLE tb_record (
    record_id INT PRIMARY KEY AUTO_INCREMENT,
    record_restaurant_id INT,
    record_person INT,
    record_time VARCHAR(50),  -- 格式: "6_12_12_35"
    FOREIGN KEY (record_restaurant_id) REFERENCES tb_restaurant(restaurant_id)
);
```

#### tb_restaurant (餐厅表)
```sql
CREATE TABLE tb_restaurant (
    restaurant_id INT PRIMARY KEY,
    restaurant_name VARCHAR(100),
    restaurant_max_capacity INT,
    restaurant_local VARCHAR(200),
    restaurant_manager_id INT
);
```

#### tb_appointment (预约表)
```sql
CREATE TABLE tb_appointment (
    appointment_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    restaurant_id INT,
    appointment_status ENUM('WAITING', 'CONFIRMED', 'CANCELLED'),
    appointment_time DATETIME,
    FOREIGN KEY (user_id) REFERENCES tb_user(user_id),
    FOREIGN KEY (restaurant_id) REFERENCES tb_restaurant(restaurant_id)
);
```


## 扩展功能

### 1. 已实现功能
- ✅ 5分钟间隔预测
- ✅ 30分钟短期预测
- ✅ 实时图表生成
- ✅ 历史数据分析
- ✅ 多餐厅支持
- ✅ 置信区间计算
- ✅ 横坐标时间5分钟倍数显示
- ✅ 纵坐标整数人数显示
- ✅ 蓝色历史+红色预测颜色区分
- ✅ 历史与预测数据连线
- ✅ 冷启动预测算法
- ✅ 动态调整机制


## 故障排除

### 常见问题

#### 1. Flask服务启动失败
```bash
# 检查端口占用
netstat -ano | findstr :5000
# 杀死占用进程
taskkill /F /PID <PID>
```

#### 2. 图表生成失败
- 检查matplotlib中文字体支持
- 确认charts目录权限
- 验证图片文件大小限制

#### 3. 时间格式错误
- 确认数据库时间格式为 "月_日_时_分"
- 检查时区设置
- 验证5分钟倍数调整逻辑



