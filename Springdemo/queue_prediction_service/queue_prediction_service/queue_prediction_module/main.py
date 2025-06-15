import sys
import argparse
import numpy as np
from queue_theory import QueueTheoryCalculator
from time_series import TimeSeriesAnalyzer

def read_historical_data():
    """从标准输入读取历史数据"""
    data = []
    for line in sys.stdin:
        try:
            value = float(line.strip())
            data.append(value)
        except ValueError:
            continue
    return np.array(data)

def main():
    parser = argparse.ArgumentParser(description='排队时间预测')
    parser.add_argument('--mode', type=str, required=True, help='预测模式：queue/flow')
    parser.add_argument('--hours', type=int, default=3, help='预测小时数')
    parser.add_argument('--confidence', type=float, default=0.95, help='置信水平')
    
    args = parser.parse_args()
    
    # 读取历史数据
    historical_data = read_historical_data()
    
    if args.mode == 'queue':
        # 使用时间序列分析进行预测
        analyzer = TimeSeriesAnalyzer(historical_data)
        predictions, intervals = analyzer.forecast(hours=args.hours, confidence_level=args.confidence)
        
        # 输出预测结果
        for pred, interval in zip(predictions, intervals):
            print(f"{pred},{interval}")
    else:
        print("不支持的预测模式", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 