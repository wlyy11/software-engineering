# software-engineering
软件工程
# 队列预测系统 - 快速开始

## 概述
本项目新增了完整的队列预测系统，实现餐厅人流量预测和等待时间估算功能。

## 核心功能

### 🔮 人流量预测系统
-  **30分钟短期预测** - 5分钟间隔，6个预测点
-  **实时图表生成** - 蓝色历史数据 + 红色预测数据
-  **冷启动算法** - 基于时间模式的智能预测

### ⏱️ 顾客排队时间系统
-  **精确等待时间** - 基于M/M/c队列理论模型
-  **置信度评估** - 提供预测可靠性指标
-  **队列位置跟踪** - 实时显示排队位置
-  **智能消息提示** - 友好的等待时间说明

### 🎯 通用功能
-  **多餐厅支持** - 支持不同餐厅的个性化预测

## 快速启动

### 1. 启动预测服务
```bash
cd queue_prediction_service
python -m flask run --host=0.0.0.0 --port=5000
```

### 2. 启动主服务
```bash
cd Springdemo
mvn spring-boot:run
```

### 3. 测试API
```bash
# 人流量预测 (30分钟预测)
curl "http://localhost:8080/api/test/peak-prediction/4/0.5"

# 顾客排队时间预测
curl "http://localhost:8080/api/test/queue-prediction/4"
```

**排队时间API响应示例**:
```json
{
  "estimatedWaitTime": 2.0,
  "confidence": 0.76,
  "message": "很快就能得到服务",
  "predictionRange": [1.76, 2.24],
  "customerPosition": 3
}
```

## 技术架构
- **后端**: Spring Boot 3.x + MySQL
- **预测服务**: Flask + Python 3.12
- **算法**: 时间序列分析 + 队列理论
- **图表**: matplotlib 

## 详细文档

### 📖 人流量预测系统
**完整技术文档**: [QUEUE_PREDICTION_SYSTEM.md](./QUEUE_PREDICTION_SYSTEM.md)

包含详细的：
- 系统架构设计
- 算法实现原理
- API使用说明
- 数据库设计

### 📖 顾客排队时间系统
**完整技术文档**: [CUSTOMER_QUEUE_TIME_SYSTEM.md](./CUSTOMER_QUEUE_TIME_SYSTEM.md)

包含详细的：
- 队列理论算法(M/M/c模型)
- 等待时间预测实现
- 置信度计算方法
- API接口说明

