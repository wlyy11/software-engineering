package com.example.springdemo.pojo;

import java.util.List;
import java.util.Map;

public class QueuePredictionResponse {
    // 等待时间预测响应
    private Double estimatedWaitTime;
    private Double confidence;
    private String message;

    // 人流量预测响应
    private List<String> timeSlots;
    private List<Integer> predictedTraffic;
    private List<Map<String, Object>> peakPeriods;
    private Map<String, Object> chartData;

    // 错误信息
    private String error;

    // Getters and Setters
    public Double getEstimatedWaitTime() {
        return estimatedWaitTime;
    }

    public void setEstimatedWaitTime(Double estimatedWaitTime) {
        this.estimatedWaitTime = estimatedWaitTime;
    }

    public Double getConfidence() {
        return confidence;
    }

    public void setConfidence(Double confidence) {
        this.confidence = confidence;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public List<String> getTimeSlots() {
        return timeSlots;
    }

    public void setTimeSlots(List<String> timeSlots) {
        this.timeSlots = timeSlots;
    }

    public List<Integer> getPredictedTraffic() {
        return predictedTraffic;
    }

    public void setPredictedTraffic(List<Integer> predictedTraffic) {
        this.predictedTraffic = predictedTraffic;
    }

    public List<Map<String, Object>> getPeakPeriods() {
        return peakPeriods;
    }

    public void setPeakPeriods(List<Map<String, Object>> peakPeriods) {
        this.peakPeriods = peakPeriods;
    }

    public Map<String, Object> getChartData() {
        return chartData;
    }

    public void setChartData(Map<String, Object> chartData) {
        this.chartData = chartData;
    }

    public String getError() {
        return error;
    }

    public void setError(String error) {
        this.error = error;
    }
}