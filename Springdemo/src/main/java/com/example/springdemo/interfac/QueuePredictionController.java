package com.example.springdemo.interfac;

import com.example.springdemo.pojo.QueuePredictionRequest;
import com.example.springdemo.pojo.QueuePredictionResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.client.RestClientException;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/queue-prediction")
public class QueuePredictionController {

    @Value("${queue.prediction.service.url}")
    private String predictionServiceUrl;

    private final RestTemplate restTemplate;


    public QueuePredictionController(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @PostMapping("/wait-time")
    public ResponseEntity<QueuePredictionResponse> predictWaitTime(@RequestBody QueuePredictionRequest request) {
        System.out.println("=== 开始处理队列预测请求 ===");
        System.out.println("预测服务URL: " + predictionServiceUrl);
        System.out.println("接收到的请求对象: " + request);

        try {
            String url = predictionServiceUrl + "/api/predict/wait-time";
            System.out.println("完整调用URL: " + url);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            System.out.println("设置请求头: " + headers);

            // 将POJO转换为Map以避免序列化问题
            Map<String, Object> requestMap = convertToMap(request);
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestMap, headers);
            System.out.println("创建HTTP实体完成，发送数据: " + requestMap);

            System.out.println("开始调用RestTemplate...");
            Map<String, Object> responseMap = restTemplate.postForObject(url, entity, Map.class);
            System.out.println("RestTemplate调用成功，响应数据: " + responseMap);

            // 将Map转换回QueuePredictionResponse
            QueuePredictionResponse response = convertToResponse(responseMap);
            return ResponseEntity.ok(response);
        } catch (RestClientException e) {
            System.err.println("RestClient异常: " + e.getMessage());
            System.err.println("异常类型: " + e.getClass().getName());
            if (e.getCause() != null) {
                System.err.println("根本原因: " + e.getCause().getMessage());
            }
            e.printStackTrace();
            QueuePredictionResponse errorResponse = new QueuePredictionResponse();
            errorResponse.setError("调用预测服务失败: " + e.getMessage());
            return ResponseEntity.status(500).body(errorResponse);
        } catch (Exception e) {
            System.err.println("其他异常: " + e.getMessage());
            System.err.println("异常类型: " + e.getClass().getName());
            if (e.getCause() != null) {
                System.err.println("根本原因: " + e.getCause().getMessage());
            }
            e.printStackTrace();
            QueuePredictionResponse errorResponse = new QueuePredictionResponse();
            errorResponse.setError("系统错误: " + e.getMessage());
            return ResponseEntity.status(500).body(errorResponse);
        }
    }

    @PostMapping("/traffic")
    public ResponseEntity<QueuePredictionResponse> predictTraffic(@RequestBody QueuePredictionRequest request) {
        String url = predictionServiceUrl + "/api/predict/traffic";

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        // 使用相同的Map转换方式
        Map<String, Object> requestMap = convertToMap(request);
        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestMap, headers);

        Map<String, Object> responseMap = restTemplate.postForObject(url, entity, Map.class);
        QueuePredictionResponse response = convertToResponse(responseMap);
        return ResponseEntity.ok(response);
    }

    private Map<String, Object> convertToMap(QueuePredictionRequest request) {
        Map<String, Object> map = new HashMap<>();
        if (request.getQueueLength() != null) map.put("queueLength", request.getQueueLength());
        if (request.getAverageServiceTime() != null) map.put("averageServiceTime", request.getAverageServiceTime());
        if (request.getActiveServers() != null) map.put("activeServers", request.getActiveServers());
        if (request.getCustomerPosition() != null) map.put("customerPosition", request.getCustomerPosition());
        if (request.getCurrentTime() != null) map.put("currentTime", request.getCurrentTime());
        if (request.getRestaurantType() != null) map.put("restaurantType", request.getRestaurantType());
        if (request.getMaxCapacity() != null) map.put("maxCapacity", request.getMaxCapacity());
        if (request.getTableCount() != null) map.put("tableCount", request.getTableCount());
        if (request.getOperatingHours() != null) map.put("operatingHours", request.getOperatingHours());
        if (request.getPeakHours() != null) map.put("peakHours", request.getPeakHours());
        if (request.getWeather() != null) map.put("weather", request.getWeather());
        if (request.getIsHoliday() != null) map.put("isHoliday", request.getIsHoliday());
        if (request.getHoursAhead() != null) map.put("hoursAhead", request.getHoursAhead());
        if (request.getCurrentTraffic() != null) map.put("currentTraffic", request.getCurrentTraffic());
        return map;
    }

    private QueuePredictionResponse convertToResponse(Map<String, Object> responseMap) {
        QueuePredictionResponse response = new QueuePredictionResponse();
        if (responseMap.containsKey("estimatedWaitTime")) {
            response.setEstimatedWaitTime(((Number) responseMap.get("estimatedWaitTime")).doubleValue());
        }
        if (responseMap.containsKey("confidence")) {
            response.setConfidence(((Number) responseMap.get("confidence")).doubleValue());
        }
        if (responseMap.containsKey("message")) {
            response.setMessage((String) responseMap.get("message"));
        }
        if (responseMap.containsKey("timeSlots")) {
            response.setTimeSlots((java.util.List<String>) responseMap.get("timeSlots"));
        }
        if (responseMap.containsKey("predictedTraffic")) {
            response.setPredictedTraffic((java.util.List<Integer>) responseMap.get("predictedTraffic"));
        }
        if (responseMap.containsKey("peakPeriods")) {
            response.setPeakPeriods((java.util.List<Map<String, Object>>) responseMap.get("peakPeriods"));
        }
        if (responseMap.containsKey("chartData")) {
            response.setChartData((Map<String, Object>) responseMap.get("chartData"));
        }
        if (responseMap.containsKey("error")) {
            response.setError((String) responseMap.get("error"));
        }
        return response;
    }
}