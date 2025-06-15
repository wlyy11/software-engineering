package com.example.springdemo.pojo;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public class QueuePredictionRequest {
    // 等待时间预测参数
    private Integer queueLength;
    private Double averageServiceTime;
    private Integer activeServers;
    private Integer customerPosition;
    private String currentTime;
    private String restaurantType;
    private Integer maxCapacity;
    private Integer tableCount;
    private List<Integer> operatingHours;
    private List<Integer> peakHours;
    private String weather;
    private Boolean isHoliday;

    // 人流量预测参数
    private Integer hoursAhead;
    private Integer currentTraffic;

    // Getters and Setters
    public Integer getQueueLength() {
        return queueLength;
    }

    public void setQueueLength(Integer queueLength) {
        this.queueLength = queueLength;
    }

    public Double getAverageServiceTime() {
        return averageServiceTime;
    }

    public void setAverageServiceTime(Double averageServiceTime) {
        this.averageServiceTime = averageServiceTime;
    }

    public Integer getActiveServers() {
        return activeServers;
    }

    public void setActiveServers(Integer activeServers) {
        this.activeServers = activeServers;
    }

    public Integer getCustomerPosition() {
        return customerPosition;
    }

    public void setCustomerPosition(Integer customerPosition) {
        this.customerPosition = customerPosition;
    }

    public String getCurrentTime() {
        return currentTime;
    }

    public void setCurrentTime(String currentTime) {
        this.currentTime = currentTime;
    }

    public String getRestaurantType() {
        return restaurantType;
    }

    public void setRestaurantType(String restaurantType) {
        this.restaurantType = restaurantType;
    }

    public Integer getMaxCapacity() {
        return maxCapacity;
    }

    public void setMaxCapacity(Integer maxCapacity) {
        this.maxCapacity = maxCapacity;
    }

    public Integer getTableCount() {
        return tableCount;
    }

    public void setTableCount(Integer tableCount) {
        this.tableCount = tableCount;
    }

    public List<Integer> getOperatingHours() {
        return operatingHours;
    }

    public void setOperatingHours(List<Integer> operatingHours) {
        this.operatingHours = operatingHours;
    }

    public List<Integer> getPeakHours() {
        return peakHours;
    }

    public void setPeakHours(List<Integer> peakHours) {
        this.peakHours = peakHours;
    }

    public String getWeather() {
        return weather;
    }

    public void setWeather(String weather) {
        this.weather = weather;
    }

    public Boolean getIsHoliday() {
        return isHoliday;
    }

    public void setIsHoliday(Boolean isHoliday) {
        this.isHoliday = isHoliday;
    }

    public Integer getHoursAhead() {
        return hoursAhead;
    }

    public void setHoursAhead(Integer hoursAhead) {
        this.hoursAhead = hoursAhead;
    }

    public Integer getCurrentTraffic() {
        return currentTraffic;
    }

    public void setCurrentTraffic(Integer currentTraffic) {
        this.currentTraffic = currentTraffic;
    }
}