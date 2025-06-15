import sys
import os

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'queue_prediction_module/src'))
print("PYTHONPATH:", src_path)
sys.path.insert(0, src_path)

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager
import numpy as np
import re

from predictors.wait_time_predictor import WaitTimePredictor
from predictors.traffic_predictor import TrafficPredictor
from models.prediction_models import QueueData, RestaurantConfig, PredictionContext

app = Flask(__name__)
CORS(app)

# 初始化预测器
wait_time_predictor = WaitTimePredictor()
traffic_predictor = TrafficPredictor()


def safe_parse_datetime(datetime_str):
    """
    安全解析时间戳字符串，处理Java生成的高精度时间戳
    将超过6位的微秒小数截断为6位，确保Python能正确解析
    """
    if not datetime_str:
        return datetime.now()

    try:
        # 使用正则表达式匹配并截断微秒部分
        # 匹配格式：YYYY-MM-DDTHH:MM:SS.微秒部分
        pattern = r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\.(\d+)'
        match = re.match(pattern, datetime_str)

        if match:
            base_time = match.group(1)  # 日期时间部分
            microseconds = match.group(2)  # 微秒部分

            # 截断微秒为最多6位
            if len(microseconds) > 6:
                microseconds = microseconds[:6]
                print(f"时间戳精度截断: {datetime_str} -> {base_time}.{microseconds}")

            # 重新组装时间戳
            truncated_datetime_str = f"{base_time}.{microseconds}"
            return datetime.fromisoformat(truncated_datetime_str)
        else:
            # 如果没有微秒部分，直接解析
            return datetime.fromisoformat(datetime_str)

    except Exception as e:
        print(f"时间戳解析失败: {datetime_str}, 错误: {e}")
        print("使用当前时间作为回退")
        return datetime.now()


@app.route('/api/predict/wait-time', methods=['POST'])
def predict_wait_time():
    print("=== Flask收到请求 ===")
    print("Content-Type:", request.content_type)
    print("Raw data:", request.data)
    print("JSON data:", request.json)
    print("Data type:", type(request.json))

    data = request.json
    if data is None:
        return jsonify({'error': 'No JSON data received'}), 400

    try:
        # 构造QueueData
        queue_data = QueueData(
            current_queue_length=data.get('queueLength', 0),
            average_service_time=data.get('averageServiceTime', 10.0),
            active_servers=data.get('activeServers', 1),
            timestamp=safe_parse_datetime(data.get('currentTime'))
        )

        # 构造RestaurantConfig
        restaurant_config = RestaurantConfig(
            restaurant_type=data.get('restaurantType', 'fast_food'),
            max_capacity=data.get('maxCapacity', 50),
            table_count=data.get('tableCount', 10),
            operating_hours=tuple(data.get('operatingHours', [8, 22])),
            peak_hours=data.get('peakHours', [12, 18])
        )

        # 构造PredictionContext
        context = PredictionContext(
            current_time=safe_parse_datetime(data.get('currentTime')),
            weather_info={'condition': data.get('weather', 'sunny')},
            is_holiday=data.get('isHoliday', False),
            local_events=[],
            special_conditions=[]
        )

        # 处理历史数据（如果提供）
        historical_data = data.get('historicalData', {})
        if historical_data:
            print("使用历史数据改进预测:", historical_data)
            # 将历史数据添加到预测器中，避免冷启动
            wait_time_predictor.add_historical_data(historical_data)

        input_data = {
            'queue_data': queue_data,
            'customer_position': data.get('customerPosition', queue_data.current_queue_length + 1),
            'restaurant_config': restaurant_config
        }

        print("预测输入数据:")
        print(f"  队列长度: {queue_data.current_queue_length}")
        print(f"  平均服务时间: {queue_data.average_service_time}")
        print(f"  活跃服务台: {queue_data.active_servers}")
        print(f"  顾客位置: {input_data['customer_position']}")
        print(f"  餐厅类型: {restaurant_config.restaurant_type}")
        print(f"  最大容量: {restaurant_config.max_capacity}")

        prediction = wait_time_predictor.predict(input_data, context)

        result = {
            'estimatedWaitTime': prediction.estimated_wait_time,
            'confidence': prediction.confidence_level,
            'message': prediction.message,
            'predictionRange': prediction.prediction_range,
            'customerPosition': prediction.customer_position,
            'timestamp': prediction.timestamp.isoformat() if prediction.timestamp else None
        }

        print("预测结果:", result)
        return jsonify(result)

    except Exception as e:
        print("预测错误:", str(e))
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict/traffic', methods=['POST'])
def predict_traffic():
    data = request.json
    try:
        # 构造RestaurantConfig
        restaurant_config = RestaurantConfig(
            restaurant_type=data.get('restaurantType', 'fast_food'),
            max_capacity=data.get('maxCapacity', 50),
            table_count=data.get('tableCount', 10),
            operating_hours=tuple(data.get('operatingHours', [8, 22])),
            peak_hours=data.get('peakHours', [12, 18])
        )
        # 构造PredictionContext
        context = PredictionContext(
            current_time=safe_parse_datetime(data.get('currentTime')),
            weather_info={'condition': data.get('weather', 'sunny')},
            is_holiday=data.get('isHoliday', False),
            local_events=[],
            special_conditions=[]
        )
        input_data = {
            'current_traffic': data.get('currentTraffic', 0),
            'prediction_hours': data.get('hoursAhead', 24),
            'predictionIntervals': data.get('predictionIntervals', 6),  # 新增：预测间隔数
            'intervalMinutes': data.get('intervalMinutes', 5),  # 新增：间隔分钟数
            'restaurant_config': restaurant_config
        }
        prediction = traffic_predictor.predict(input_data, context)

        # 生成图表
        chart_filename = None
        try:
            chart_filename = generate_traffic_chart(data, prediction, context)
            print(f"图表已生成: {chart_filename}")
        except Exception as chart_error:
            print(f"图表生成失败: {chart_error}")

        return jsonify({
            'timeSlots': prediction.time_slots,
            'predictedTraffic': prediction.predicted_traffic,
            'peakPeriods': prediction.peak_periods,
            'chartData': prediction.chart_data,
            'chartFilename': chart_filename,
            'algorithmUsed': 'TrafficPredictor with Time Series Analysis'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def generate_traffic_chart(request_data, prediction, context):
    """
    生成人流预测图表
    """
    try:
        # 创建图表目录
        chart_dir = os.path.join(os.path.dirname(__file__), 'charts')
        os.makedirs(chart_dir, exist_ok=True)

        # 设置matplotlib使用非交互式后端
        plt.switch_backend('Agg')

        # 创建图表
        fig, ax = plt.subplots(figsize=(14, 8))

        # 获取历史数据（最近3条记录，约15分钟）
        historical_data = request_data.get('historicalData', {})
        recent_counts = historical_data.get('recentTrafficCounts', [])
        recent_timestamps = historical_data.get('recentTimestamps', [])

        # 生成历史数据的时间点
        current_time = context.current_time
        past_times = []
        past_counts = []

        # 处理最近的数据（5分钟间隔）
        if recent_counts and recent_timestamps:
            print(f"处理最近数据: {len(recent_counts)} 条记录")
            print(f"时间戳: {recent_timestamps}")
            print(f"人流数: {recent_counts}")

            # 直接解析数据库时间戳，格式：月_日_时_分
            for i, (count, timestamp) in enumerate(zip(recent_counts, recent_timestamps)):
                try:
                    # 解析时间戳格式：6_12_12_25 -> 6月12日12时25分
                    parts = timestamp.split('_')
                    if len(parts) == 4:
                        month, day, hour, minute = map(int, parts)
                        # 使用当前年份
                        year = current_time.year
                        past_time = datetime(year, month, day, hour, minute)
                        past_times.append(past_time)
                        past_counts.append(int(count))  # 确保历史数据为整数
                        print(f"历史点 {i + 1}: {past_time.strftime('%H:%M')} -> {count}人")
                    else:
                        print(f"无法解析时间戳: {timestamp}")
                except Exception as e:
                    print(f"解析时间戳 {timestamp} 失败: {e}")
                    # 如果解析失败，使用回退方案
                    minutes_ago = (len(recent_counts) - 1 - i) * 5
                    past_time = current_time - timedelta(minutes=minutes_ago)
                    adjusted_minute = (past_time.minute // 5) * 5
                    past_time = past_time.replace(minute=adjusted_minute, second=0, microsecond=0)
                    past_times.append(past_time)
                    past_counts.append(int(count))  # 确保历史数据为整数
                    print(f"历史点 {i + 1} (回退): {past_time.strftime('%H:%M')} -> {count}人")

        # 获取预测数据
        future_times = []
        future_counts = [int(round(count)) for count in prediction.predicted_traffic]  # 确保预测数据为整数

        # 生成未来时间点（支持分钟间隔），从下一个5分钟时刻开始
        interval_minutes = request_data.get('intervalMinutes', 5)

        # 计算下一个5分钟时刻作为预测起点
        current_minute = current_time.minute
        next_5min_minute = ((current_minute // 5) + 1) * 5

        if next_5min_minute >= 60:
            next_start_time = current_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        else:
            next_start_time = current_time.replace(minute=next_5min_minute, second=0, microsecond=0)

        print(f"预测起始时间: {current_time.strftime('%H:%M')} -> {next_start_time.strftime('%H:%M')}")

        for i, time_slot in enumerate(prediction.time_slots):
            future_time = next_start_time + timedelta(minutes=i * interval_minutes)
            future_times.append(future_time)
            print(
                f"预测点 {i + 1}: {future_time.strftime('%H:%M')} -> {future_counts[i] if i < len(future_counts) else 0}人")

        # 绘制历史数据（蓝色实线）
        if past_times and past_counts:
            ax.plot(past_times, past_counts, 'b-', linewidth=2, marker='o',
                    markersize=6, label='Historical Data (Past 15 Minutes)', alpha=0.8)

            # 标注历史数据点的数值
            for time, count in zip(past_times, past_counts):
                ax.annotate(f'{count}', (time, count), textcoords="offset points",
                            xytext=(0, 10), ha='center', fontsize=9, color='blue')

        # 绘制预测数据（红色实线），包括从历史到预测的连接
        if future_times and future_counts:
            # 如果有历史数据，从最后一个历史点连接到第一个预测点
            if past_times and past_counts:
                # 连接历史数据的最后一点到预测数据的第一点
                connection_times = [past_times[-1], future_times[0]]
                connection_counts = [past_counts[-1], future_counts[0]]
                ax.plot(connection_times, connection_counts, 'r-', linewidth=2, alpha=0.8)

            # 绘制预测数据线
            ax.plot(future_times, future_counts, 'r-', linewidth=2, marker='s',
                    markersize=6, label='Predicted Traffic', alpha=0.8)

            # 标注预测数据点的数值
            for time, count in zip(future_times, future_counts):
                ax.annotate(f'{count}', (time, count), textcoords="offset points",
                            xytext=(0, 10), ha='center', fontsize=9, color='red')

        # 标注当前时间点
        current_traffic = request_data.get('currentTraffic', 0)
        ax.plot(current_time, current_traffic, 'go', markersize=10,
                label=f'Current Time ({current_traffic} people)')
        ax.annotate(f'NOW\n{current_traffic}', (current_time, current_traffic),
                    textcoords="offset points", xytext=(0, 15), ha='center',
                    fontsize=10, fontweight='bold', color='green')

        # 高峰时段标注
        if prediction.peak_periods:
            for peak in prediction.peak_periods:
                start_time_str = peak.get('start_time', '')
                end_time_str = peak.get('end_time', '')
                peak_traffic = peak.get('peak_traffic', 0)

                try:
                    start_time = safe_parse_datetime(start_time_str.replace('Z', '+00:00'))
                    ax.axvspan(start_time, start_time + timedelta(hours=1),
                               alpha=0.2, color='orange', label='Peak Period')
                except:
                    pass

        # 设置图表标题和标签
        restaurant_id = request_data.get('restaurantId', 'N/A')

        ax.set_title(f'Traffic prediction for id: {restaurant_id}', fontsize=14, fontweight='bold')
        ax.set_xlabel('Time', fontsize=12)
        ax.set_ylabel('Number of People', fontsize=12)

        # 设置时间轴格式 - 强制显示我们想要的时间点
        all_times = past_times + future_times
        if all_times:
            # 手动设置X轴刻度为实际的数据点时间
            ax.set_xticks(all_times)
            ax.set_xticklabels([t.strftime('%H:%M') for t in all_times], rotation=45)

        # 设置Y轴只显示整数
        from matplotlib.ticker import MaxNLocator
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        # 设置网格和图例
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper left')

        # 设置Y轴从0开始
        ax.set_ylim(bottom=0)

        # 调整布局
        plt.tight_layout()

        # 生成文件名（包含时间戳）
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'traffic_prediction_{restaurant_id}_{timestamp}.png'
        filepath = os.path.join(chart_dir, filename)

        # 保存图表
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"图表已保存到: {filepath}")
        return filename

    except Exception as e:
        print(f"生成图表时出错: {e}")
        import traceback
        traceback.print_exc()
        return None


@app.route('/api/chart/<filename>')
def get_chart(filename):
    """
    获取生成的图表文件
    """
    try:
        chart_dir = os.path.join(os.path.dirname(__file__), 'charts')
        filepath = os.path.join(chart_dir, filename)

        if os.path.exists(filepath):
            from flask import send_file
            return send_file(filepath, mimetype='image/png')
        else:
            return jsonify({'error': 'Chart not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 