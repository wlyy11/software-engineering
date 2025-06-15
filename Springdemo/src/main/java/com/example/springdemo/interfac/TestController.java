package com.example.springdemo.interfac;

import com.example.springdemo.pojo.Appointment;
import com.example.springdemo.pojo.DataRecord;
import com.example.springdemo.pojo.Restaurant;
import com.example.springdemo.repo.AppointRepo;
import com.example.springdemo.repo.DataRecordRepo;
import com.example.springdemo.repo.RestaurantRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/test")
public class TestController {

    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    private DataRecordRepo dataRecordRepo;

    @Autowired
    private RestaurantRepo restaurantRepo;

    @Autowired
    private AppointRepo appointRepo;

    @GetMapping("/flask")
    public ResponseEntity<String> testFlask() {
        try {
            System.out.println("测试Flask连接...");
            String url = "http://127.0.0.1:5000/api/predict/wait-time";

            // 创建正确的HTTP请求
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            String jsonBody = "{\"queueLength\": 5}";
            HttpEntity<String> entity = new HttpEntity<>(jsonBody, headers);

            System.out.println("URL: " + url);
            System.out.println("Body: " + jsonBody);
            System.out.println("Headers: " + headers);

            String response = restTemplate.postForObject(url, entity, String.class);
            System.out.println("Flask响应: " + response);

            return ResponseEntity.ok("Flask测试成功: " + response);
        } catch (Exception e) {
            System.err.println("Flask测试失败: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(500).body("Flask测试失败: " + e.getMessage());
        }
    }

    @GetMapping("/queue-prediction")
    public ResponseEntity<String> testQueuePrediction() {
        return testQueuePredictionForRestaurant(4); // 默认使用餐厅ID=4
    }

    @GetMapping("/queue-prediction/{restaurantId}")
    public ResponseEntity<String> testQueuePredictionForRestaurant(@PathVariable int restaurantId) {
        try {
            System.out.println("测试餐厅 " + restaurantId + " 的队列预测...");

            // 1. 获取餐厅信息
            Optional<Restaurant> restaurantOpt = restaurantRepo.findById(restaurantId);
            if (!restaurantOpt.isPresent()) {
                return ResponseEntity.status(404).body("餐厅不存在: " + restaurantId);
            }
            Restaurant restaurant = restaurantOpt.get();

            // 2. 获取最新的人流记录
            Optional<DataRecord> latestRecordOpt = dataRecordRepo.findLatestRecord(restaurantId);
            if (!latestRecordOpt.isPresent()) {
                return ResponseEntity.status(404).body("餐厅 " + restaurantId + " 没有人流记录");
            }
            DataRecord latestRecord = latestRecordOpt.get();

            // 3. 获取当前等待的去重用户数量（真正的排队人数）
            int uniqueWaitingUsers = appointRepo.countUniqueWaitingUsersByRestaurant(restaurantId);

            // 4. 获取历史记录用于计算平均服务时间
            List<DataRecord> recentRecords = dataRecordRepo.findNRecord(10, restaurantId);
            double averageServiceTime = calculateAverageServiceTime(recentRecords);

            // 5. 估算活跃服务台数量（基于餐厅容量）
            int activeServers = Math.max(1, restaurant.getMaxCapacity() / 25); // 假设每25个座位需要1个服务台

            // 6. 构建预测请求数据
            String url = "http://127.0.0.1:5000/api/predict/wait-time";
            Map<String, Object> requestData = new HashMap<>();

            // 修正逻辑：record中的人数是正在食堂里的人数，排队人数就是等待预约的去重用户数
            requestData.put("queueLength", uniqueWaitingUsers); // 真正的排队人数
            requestData.put("averageServiceTime", averageServiceTime);
            requestData.put("activeServers", activeServers);
            requestData.put("customerPosition", uniqueWaitingUsers + 1); // 新顾客排在队尾
            requestData.put("currentTime", LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
            requestData.put("restaurantType", determineRestaurantType(restaurant));
            requestData.put("maxCapacity", restaurant.getMaxCapacity());
            requestData.put("tableCount", restaurant.getMaxCapacity() / 4); // 假设每桌4人
            requestData.put("weather", "晴天"); // 可以后续接入天气API
            requestData.put("isHoliday", isHoliday());

            // 添加历史数据用于改进预测
            requestData.put("historicalData", buildHistoricalData(recentRecords));

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestData, headers);

            System.out.println("餐厅信息: " + restaurant);
            System.out.println("最新人流: " + latestRecord);
            System.out.println("排队等待用户: " + uniqueWaitingUsers + " 个");
            System.out.println("发送预测数据: " + requestData);

            // 调用Flask预测服务
            Map<String, Object> response = restTemplate.postForObject(url, entity, Map.class);
            System.out.println("Flask响应: " + response);

            return ResponseEntity.ok(String.format(
                    "餐厅 %s (ID:%d) 队列预测成功:\n" +
                            "食堂内人数: %d 人\n" +
                            "排队等待用户: %d 个\n" +
                            "预测结果: %s",
                    restaurant.getName(), restaurantId, latestRecord.getPerson(),
                    uniqueWaitingUsers, response.toString()
            ));

        } catch (Exception e) {
            System.err.println("队列预测失败: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(500).body("队列预测失败: " + e.getMessage());
        }
    }

    @GetMapping("/queue-prediction/user/{userId}")
    public ResponseEntity<String> getUserQueuePrediction(@PathVariable int userId) {
        try {
            System.out.println("查询用户 " + userId + " 的个性化队列预测...");

            // 1. 查找用户的等待中预约
            Optional<Appointment> userAppointmentOpt = appointRepo.findUserWaitingAppointment(userId);
            if (!userAppointmentOpt.isPresent()) {
                return ResponseEntity.status(404).body("用户 " + userId + " 没有等待中的预约");
            }

            Appointment userAppointment = userAppointmentOpt.get();
            int restaurantId = userAppointment.getRestaurant().getId();
            Restaurant restaurant = userAppointment.getRestaurant();

            System.out.println("用户预约信息: " + userAppointment);

            // 2. 获取最新的人流记录
            Optional<DataRecord> latestRecordOpt = dataRecordRepo.findLatestRecord(restaurantId);
            if (!latestRecordOpt.isPresent()) {
                return ResponseEntity.status(404).body("餐厅 " + restaurantId + " 没有人流记录");
            }
            DataRecord latestRecord = latestRecordOpt.get();

            // 3. 计算用户在总队列中的实际位置
            int userActualPosition = calculateUserActualPosition(userId, restaurantId);
            if (userActualPosition == -1) {
                return ResponseEntity.status(404).body("无法确定用户在队列中的位置");
            }

            // 4. 获取历史记录用于计算平均服务时间
            List<DataRecord> recentRecords = dataRecordRepo.findNRecord(10, restaurantId);
            double averageServiceTime = calculateAverageServiceTime(recentRecords);

            // 5. 估算活跃服务台数量（基于餐厅容量）
            int activeServers = Math.max(1, restaurant.getMaxCapacity() / 25);

            // 6. 获取当前等待的去重用户数量
            int uniqueWaitingUsers = appointRepo.countUniqueWaitingUsersByRestaurant(restaurantId);

            // 7. 构建预测请求数据（复用现有算法）
            String url = "http://127.0.0.1:5000/api/predict/wait-time";
            Map<String, Object> requestData = new HashMap<>();

            // 修正逻辑：排队人数就是等待预约的去重用户数
            requestData.put("queueLength", uniqueWaitingUsers);
            requestData.put("averageServiceTime", averageServiceTime);
            requestData.put("activeServers", activeServers);
            requestData.put("customerPosition", userActualPosition); // 关键：用户的实际排队位置
            requestData.put("currentTime", LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
            requestData.put("restaurantType", determineRestaurantType(restaurant));
            requestData.put("maxCapacity", restaurant.getMaxCapacity());
            requestData.put("tableCount", restaurant.getMaxCapacity() / 4);
            requestData.put("weather", "晴天");
            requestData.put("isHoliday", isHoliday());

            // 添加历史数据用于改进预测
            requestData.put("historicalData", buildHistoricalData(recentRecords));

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestData, headers);

            System.out.println("用户实际排队位置: " + userActualPosition);
            System.out.println("食堂内人数: " + latestRecord.getPerson());
            System.out.println("排队等待用户数: " + uniqueWaitingUsers);
            System.out.println("发送预测数据: " + requestData);

            // 调用Flask预测服务（完全相同的算法）
            Map<String, Object> response = restTemplate.postForObject(url, entity, Map.class);
            System.out.println("Flask响应: " + response);

            return ResponseEntity.ok(String.format(
                    "用户 %d 在餐厅 %s (ID:%d) 的个性化排队预测:\n" +
                            "食堂内人数: %d 人\n" +
                            "排队等待用户数: %d 个\n" +
                            "您的实际排队位置: 第 %d 位\n" +
                            "预测结果: %s",
                    userId, restaurant.getName(), restaurantId,
                    latestRecord.getPerson(), uniqueWaitingUsers, userActualPosition,
                    response.toString()
            ));

        } catch (Exception e) {
            System.err.println("用户队列预测失败: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(500).body("用户队列预测失败: " + e.getMessage());
        }
    }

    /**
     * 计算平均服务时间（基于历史人流变化）
     */
    private double calculateAverageServiceTime(List<DataRecord> records) {
        if (records.size() < 2) {
            return 10.0; // 默认15分钟
        }

        // 简化计算：基于人流变化推算服务时间
        double totalServiceTime = 0;
        int validPairs = 0;

        for (int i = 0; i < records.size() - 1; i++) {
            DataRecord current = records.get(i);
            DataRecord previous = records.get(i + 1);

            // 如果人数减少，说明有人被服务完成
            if (previous.getPerson() > current.getPerson()) {
                int servedPeople = previous.getPerson() - current.getPerson();
                // 假设记录间隔为5分钟，计算每人平均服务时间
                double serviceTimePerPerson = 5.0 / Math.max(1, servedPeople);
                totalServiceTime += serviceTimePerPerson;
                validPairs++;
            }
        }

        if (validPairs > 0) {
            return Math.max(5.0, Math.min(30.0, totalServiceTime / validPairs)); // 限制在5-30分钟
        }

        return 15.0; // 默认值
    }

    /**
     * 根据餐厅容量判断餐厅类型
     */
    private String determineRestaurantType(Restaurant restaurant) {
        int capacity = restaurant.getMaxCapacity();
        if (capacity <= 30) {
            return "快餐";
        } else if (capacity <= 80) {
            return "休闲餐厅";
        } else {
            return "大型餐厅";
        }
    }

    /**
     * 判断是否为节假日（简化实现）
     */
    private boolean isHoliday() {
        LocalDateTime now = LocalDateTime.now();
        int dayOfWeek = now.getDayOfWeek().getValue();
        return dayOfWeek == 6 || dayOfWeek == 7; // 周末视为节假日
    }

    /**
     * 构建历史数据用于预测算法
     */
    private Map<String, Object> buildHistoricalData(List<DataRecord> records) {
        Map<String, Object> historicalData = new HashMap<>();

        if (!records.isEmpty()) {
            // 计算人流趋势
            int[] personCounts = records.stream().mapToInt(DataRecord::getPerson).toArray();
            historicalData.put("recentPersonCounts", personCounts);

            // 计算平均人流
            double avgPerson = records.stream().mapToInt(DataRecord::getPerson).average().orElse(0);
            historicalData.put("averagePersonCount", avgPerson);

            // 计算人流波动
            double variance = records.stream()
                    .mapToDouble(r -> Math.pow(r.getPerson() - avgPerson, 2))
                    .average().orElse(0);
            historicalData.put("personCountVariance", variance);
        }

        return historicalData;
    }

    /**
     * 计算用户在排队中的实际位置
     */
    private int calculateUserActualPosition(int userId, int restaurantId) {
        try {
            // 获取所有等待预约，然后在Java中去重和排序
            List<Appointment> allWaitingAppointments = appointRepo.findWaitingAppointmentsByRestaurantOrderByTime(restaurantId);

            // 手动去重：每个用户只保留最早的预约（按ID排序，因为时间为null）
            Map<Integer, Appointment> userEarliestAppointments = new HashMap<>();
            for (Appointment appointment : allWaitingAppointments) {
                int currentUserId = appointment.getUser().getId();
                if (!userEarliestAppointments.containsKey(currentUserId) ||
                        appointment.getId() < userEarliestAppointments.get(currentUserId).getId()) {
                    userEarliestAppointments.put(currentUserId, appointment);
                }
            }

            // 按预约ID排序（因为时间为null，用ID代替）
            java.util.List<Appointment> uniqueWaitingQueue = new java.util.ArrayList<>(userEarliestAppointments.values());
            uniqueWaitingQueue.sort((a, b) -> Integer.compare(a.getId(), b.getId()));

            // 找到用户在去重队列中的位置
            int userPositionInQueue = -1;
            for (int i = 0; i < uniqueWaitingQueue.size(); i++) {
                if (uniqueWaitingQueue.get(i).getUser().getId() == userId) {
                    userPositionInQueue = i + 1; // 1-based position
                    break;
                }
            }

            if (userPositionInQueue == -1) {
                return -1; // 用户不在等待队列中
            }

            System.out.println("位置计算详情:");
            System.out.println("  原始等待预约数: " + allWaitingAppointments.size());
            System.out.println("  去重后排队用户数: " + uniqueWaitingQueue.size());
            System.out.println("  用户在排队中的位置: " + userPositionInQueue);

            return userPositionInQueue;

        } catch (Exception e) {
            System.err.println("计算用户位置失败: " + e.getMessage());
            e.printStackTrace();
            return -1;
        }
    }

    @GetMapping("/hello")
    public ResponseEntity<String> hello() {
        return ResponseEntity.ok("Hello from Test Controller!");
    }

    @GetMapping("/debug/appointments/{restaurantId}")
    public ResponseEntity<String> debugAppointments(@PathVariable int restaurantId) {
        try {
            // 查看所有预约数据
            List<Appointment> allAppointments = appointRepo.findWaitingAppointmentsByRestaurantOrderByTime(restaurantId);

            StringBuilder result = new StringBuilder();
            result.append("餐厅 ").append(restaurantId).append(" 的所有等待预约:\n");
            result.append("总数: ").append(allAppointments.size()).append("\n\n");

            for (int i = 0; i < allAppointments.size(); i++) {
                Appointment app = allAppointments.get(i);
                result.append(String.format("预约 %d:\n", i + 1));
                result.append(String.format("  用户ID: %d\n", app.getUser().getId()));
                result.append(String.format("  预约时间: %s\n", app.getTime()));
                result.append(String.format("  状态: %s\n", app.getStatus()));
                result.append("\n");
            }

            // 测试去重统计
            int uniqueCount = appointRepo.countUniqueWaitingUsersByRestaurant(restaurantId);
            result.append("去重用户数: ").append(uniqueCount).append("\n");

            return ResponseEntity.ok(result.toString());

        } catch (Exception e) {
            return ResponseEntity.status(500).body("调试失败: " + e.getMessage());
        }
    }

    @GetMapping("/debug/user/{userId}")
    public ResponseEntity<String> debugUserAppointment(@PathVariable int userId) {
        try {
            Optional<Appointment> userAppointment = appointRepo.findUserWaitingAppointment(userId);

            if (userAppointment.isPresent()) {
                Appointment app = userAppointment.get();
                return ResponseEntity.ok(String.format(
                        "用户 %d 的等待预约:\n" +
                                "预约ID: %d\n" +
                                "餐厅ID: %d\n" +
                                "预约时间: %s\n" +
                                "状态: %s",
                        userId, app.getId(), app.getRestaurant().getId(),
                        app.getTime(), app.getStatus()
                ));
            } else {
                return ResponseEntity.ok("用户 " + userId + " 没有等待中的预约");
            }

        } catch (Exception e) {
            return ResponseEntity.status(500).body("调试失败: " + e.getMessage());
        }
    }

    @GetMapping("/peak-prediction/{restaurantId}/{hoursAhead}")
    public ResponseEntity<Map<String, Object>> predictPeakHours(@PathVariable int restaurantId, @PathVariable double hoursAhead) {
        try {
            System.out.println("开始预测餐厅 " + restaurantId + " 未来 " + hoursAhead + " 小时的人流高峰...");

            // 1. 获取餐厅信息
            Optional<Restaurant> restaurantOpt = restaurantRepo.findById(restaurantId);
            if (!restaurantOpt.isPresent()) {
                Map<String, Object> errorResponse = new HashMap<>();
                errorResponse.put("error", "餐厅不存在: " + restaurantId);
                return ResponseEntity.status(404).body(errorResponse);
            }
            Restaurant restaurant = restaurantOpt.get();

            // 2. 获取最新的人流记录作为当前流量
            Optional<DataRecord> latestRecordOpt = dataRecordRepo.findLatestRecord(restaurantId);
            if (!latestRecordOpt.isPresent()) {
                Map<String, Object> errorResponse = new HashMap<>();
                errorResponse.put("error", "餐厅 " + restaurantId + " 没有人流记录");
                return ResponseEntity.status(404).body(errorResponse);
            }
            DataRecord latestRecord = latestRecordOpt.get();

            // 3. 获取历史记录用于模式分析和图表显示
            List<DataRecord> allHistoricalRecords = dataRecordRepo.findNRecord(50, restaurantId); // 获取更多历史数据用于模式分析
            List<DataRecord> recentRecords = dataRecordRepo.findNRecord(8, restaurantId); // 获取最近3条记录用于图表显示（15分钟）

            // 4. 构建预测请求数据
            String url = "http://127.0.0.1:5000/api/predict/traffic";
            Map<String, Object> requestData = new HashMap<>();

            int pre = (int) (hoursAhead * 60.0f) / 5;

            // 基础数据
            requestData.put("restaurantId", restaurantId);
            requestData.put("restaurantName", restaurant.getName()); // 添加餐厅名称用于图表
            requestData.put("currentTraffic", latestRecord.getPerson());
            requestData.put("hoursAhead", hoursAhead);
            requestData.put("predictionIntervals", pre); // 预测pre个间隔（30分钟）
            requestData.put("intervalMinutes", 5); // 每个间隔5分钟
            // 使用数据库最新记录时间作为预测起点
            requestData.put("currentTime", parseRecordTimeToISO(latestRecord.getTime()));
            requestData.put("restaurantType", determineRestaurantType(restaurant));
            requestData.put("maxCapacity", restaurant.getMaxCapacity());
            requestData.put("tableCount", restaurant.getMaxCapacity() / 4);
            requestData.put("operatingHours", Arrays.asList(8, 20)); // 营业时间 8:00-22:00
            requestData.put("peakHours", Arrays.asList(12, 18, 19)); // 默认高峰时段
            requestData.put("weather", "晴天");
            requestData.put("isHoliday", isHoliday());

            // 添加历史数据用于模式识别和图表生成
            requestData.put("historicalData", buildTrafficHistoricalData(allHistoricalRecords, recentRecords));

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestData, headers);

            System.out.println("餐厅信息: " + restaurant);
            System.out.println("当前人流: " + latestRecord.getPerson() + " 人");
            System.out.println("预测时长: " + hoursAhead + " 小时");
            System.out.println("历史记录数: " + allHistoricalRecords.size() + " 条");
            System.out.println("图表显示记录数: " + recentRecords.size() + " 条");
            System.out.println("发送预测数据: " + requestData);

            // 调用Flask人流预测服务（现在会同时生成图表）
            Map<String, Object> response = restTemplate.postForObject(url, entity, Map.class);
            System.out.println("Flask响应: " + response);

            // 构建返回的JSON响应
            Map<String, Object> result = new HashMap<>();
            Map<String, Object> result1 = new HashMap<>();

            result.put("restaurantId", restaurantId);
            result.put("restaurantName", restaurant.getName());
            result.put("currentTraffic", latestRecord.getPerson());
            result.put("hoursAhead", hoursAhead);
            result.put("predictionTime", LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));

            // 预测数据
            result.put("timeSlots", response.get("timeSlots"));
            result.put("predictedTraffic", response.get("predictedTraffic"));
            result.put("peakPeriods", response.get("peakPeriods"));
            result.put("chartData", response.get("chartData"));

            // 图表信息
            String chartFilename = (String) response.get("chartFilename");
            String algorithmUsed = (String) response.get("algorithmUsed");

            result.put("chartFilename", chartFilename);
            result.put("chartUrl", chartFilename != null ?
                    "http://localhost:5000/api/chart/" + chartFilename : null);
            result.put("algorithm", algorithmUsed != null ? algorithmUsed :
                    "TrafficPredictor with Time Series Analysis");

            // 生成用户友好的预测摘要
            result.put("summary", formatTrafficPredictionSummary(restaurant, latestRecord, hoursAhead, response));

            // 图表状态信息
            if (chartFilename != null) {
                result.put("chartStatus", "图表已生成");
                result.put("chartInfo", String.format("图表文件: %s, 可通过 %s 访问",
                        chartFilename, "http://localhost:5000/api/chart/" + chartFilename));
            } else {
                result.put("chartStatus", "图表生成失败");
            }

            return ResponseEntity.ok(result);

        } catch (Exception e) {
            System.err.println("高峰期预测失败: " + e.getMessage());
            e.printStackTrace();
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("error", "高峰期预测失败: " + e.getMessage());
            return ResponseEntity.status(500).body(errorResponse);
        }
    }

    /**
     * 构建人流预测的历史数据
     */
    private Map<String, Object> buildTrafficHistoricalData(List<DataRecord> allRecords, List<DataRecord> recentRecords) {
        Map<String, Object> historicalData = new HashMap<>();

        // 用于模式分析的所有历史数据
        if (!allRecords.isEmpty()) {
            List<Integer> allTrafficCounts = new ArrayList<>();
            List<String> allTimestamps = new ArrayList<>();

            for (DataRecord record : allRecords) {
                allTrafficCounts.add(record.getPerson());
                allTimestamps.add(record.getTime());
            }

            // 计算统计信息（用于模式分析）
            double averageTraffic = allTrafficCounts.stream().mapToInt(Integer::intValue).average().orElse(0.0);
            int maxTraffic = allTrafficCounts.stream().mapToInt(Integer::intValue).max().orElse(0);
            int minTraffic = allTrafficCounts.stream().mapToInt(Integer::intValue).min().orElse(0);

            // 计算方差
            double variance = allTrafficCounts.stream()
                    .mapToDouble(count -> Math.pow(count - averageTraffic, 2))
                    .average().orElse(0.0);

            historicalData.put("allTrafficCounts", allTrafficCounts);
            historicalData.put("allTimestamps", allTimestamps);
            historicalData.put("averageTraffic", averageTraffic);
            historicalData.put("maxTraffic", maxTraffic);
            historicalData.put("minTraffic", minTraffic);
            historicalData.put("trafficVariance", variance);
            historicalData.put("recordCount", allRecords.size());

            System.out.println("历史数据统计:");
            System.out.println("  记录数量: " + allRecords.size());
            System.out.println("  平均人流: " + String.format("%.1f", averageTraffic));
            System.out.println("  最大人流: " + maxTraffic);
            System.out.println("  最小人流: " + minTraffic);
            System.out.println("  人流方差: " + String.format("%.2f", variance));
        }

        // 用于图表显示的最近数据（最近3条记录，约15分钟）
        if (!recentRecords.isEmpty()) {
            List<Integer> recentTrafficCounts = new ArrayList<>();
            List<String> recentTimestamps = new ArrayList<>();

            // 注意：recentRecords是按时间倒序的，需要反转为正序
            for (int i = recentRecords.size() - 1; i >= 0; i--) {
                DataRecord record = recentRecords.get(i);
                recentTrafficCounts.add(record.getPerson());
                recentTimestamps.add(record.getTime());
            }

            historicalData.put("recentTrafficCounts", recentTrafficCounts);
            historicalData.put("recentTimestamps", recentTimestamps);
            historicalData.put("recentRecordCount", recentRecords.size());

            System.out.println("最近数据统计:");
            System.out.println("  最近记录数: " + recentRecords.size());
            System.out.println("  最近人流: " + recentTrafficCounts);
        }

        return historicalData;
    }

    /**
     * 解析数据库记录时间格式为ISO格式
     * 数据库格式：12_12_23_35 (月份_日_小时_分钟)
     */
    private String parseRecordTimeToISO(String recordTime) {
        try {
            if (recordTime == null || recordTime.isEmpty()) {
                return LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
            }

            // 解析格式：12_12_23_35 -> 12月12日23时35分
            String[] parts = recordTime.split("_");
            if (parts.length >= 4) {
                int month = Integer.parseInt(parts[0]);  // 第一个是月份
                int day = Integer.parseInt(parts[1]);    // 第二个是日
                int hour = Integer.parseInt(parts[2]);   // 第三个是小时
                int minute = Integer.parseInt(parts[3]); // 第四个是分钟

                // 假设是当前年份
                int year = LocalDateTime.now().getYear();
                LocalDateTime recordDateTime = LocalDateTime.of(year, month, day, hour, minute);

                // 将分钟数调整为5的倍数
                int adjustedMinute = (minute / 5) * 5;  // 向下取整到最近的5分钟
                LocalDateTime adjustedDateTime = LocalDateTime.of(year, month, day, hour, adjustedMinute);

                System.out.println("解析记录时间: " + recordTime + " -> " + adjustedDateTime + " (调整到5分钟倍数)");
                return adjustedDateTime.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
            }
        } catch (Exception e) {
            System.err.println("解析记录时间失败: " + recordTime + ", 错误: " + e.getMessage());
        }

        // 解析失败时使用当前时间
        return LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
    }

    /**
     * 生成人流预测摘要（用于JSON响应）
     */
    private String formatTrafficPredictionSummary(Restaurant restaurant, DataRecord currentRecord,
                                                  double hoursAhead, Map<String, Object> response) {
        StringBuilder summary = new StringBuilder();

        summary.append(String.format("餐厅 %s 当前有 %d 人，", restaurant.getName(), currentRecord.getPerson()));

        // 解析时间段和预测人流
        @SuppressWarnings("unchecked")
        List<String> timeSlots = (List<String>) response.get("timeSlots");
        @SuppressWarnings("unchecked")
        List<Integer> predictedTraffic = (List<Integer>) response.get("predictedTraffic");
        @SuppressWarnings("unchecked")
        List<Map<String, Object>> peakPeriods = (List<Map<String, Object>>) response.get("peakPeriods");

        if (timeSlots != null && predictedTraffic != null && !timeSlots.isEmpty()) {
            summary.append("未来预测：");
            for (int i = 0; i < Math.min(timeSlots.size(), 3); i++) {
                String timeSlot = timeSlots.get(i);
                Integer traffic = predictedTraffic.get(i);
                // 简化时间显示
                String simpleTime = timeSlot.length() > 16 ? timeSlot.substring(11, 16) : timeSlot;
                summary.append(String.format(" %s→%d人", simpleTime, traffic));
                if (i < Math.min(timeSlots.size(), 3) - 1) summary.append(",");
            }
        }

        if (peakPeriods != null && !peakPeriods.isEmpty()) {
            summary.append("。高峰时段：");
            for (int i = 0; i < Math.min(peakPeriods.size(), 2); i++) {
                Map<String, Object> peak = peakPeriods.get(i);
                String startTime = (String) peak.get("start_time");
                Integer peakTraffic = (Integer) peak.get("peak_traffic");
                if (startTime != null && peakTraffic != null) {
                    String simpleTime = startTime.length() > 16 ? startTime.substring(11, 16) : startTime;
                    summary.append(String.format(" %s→%d人", simpleTime, peakTraffic));
                    if (i < Math.min(peakPeriods.size(), 2) - 1) summary.append(",");
                }
            }
        }

        return summary.toString();
    }

    /**
     * 格式化人流预测结果
     */
    private String formatTrafficPredictionResult(Restaurant restaurant, DataRecord currentRecord,
                                                 double hoursAhead, Map<String, Object> response) {
        StringBuilder result = new StringBuilder();

        result.append(String.format("餐厅 %s (ID:%d) 高峰期预测:\n", restaurant.getName(), restaurant.getId()));
        result.append(String.format("当前人流: %d 人\n", currentRecord.getPerson()));
        result.append(String.format("预测时长: %.1f 小时\n\n", hoursAhead));

        // 解析时间段和预测人流
        @SuppressWarnings("unchecked")
        List<String> timeSlots = (List<String>) response.get("timeSlots");
        @SuppressWarnings("unchecked")
        List<Integer> predictedTraffic = (List<Integer>) response.get("predictedTraffic");
        @SuppressWarnings("unchecked")
        List<Map<String, Object>> peakPeriods = (List<Map<String, Object>>) response.get("peakPeriods");

        if (timeSlots != null && predictedTraffic != null) {
            result.append("时间段预测:\n");
            for (int i = 0; i < Math.min(timeSlots.size(), predictedTraffic.size()); i++) {
                String timeSlot = timeSlots.get(i);
                Integer traffic = predictedTraffic.get(i);

                // 简化时间显示（只显示时分）
                String displayTime = timeSlot.length() > 16 ? timeSlot.substring(11, 16) : timeSlot;
                result.append(String.format("%s → %d人\n", displayTime, traffic));
            }
        }

        // 显示高峰时段
        if (peakPeriods != null && !peakPeriods.isEmpty()) {
            result.append("\n高峰时段分析:\n");
            for (Map<String, Object> peak : peakPeriods) {
                String startTime = (String) peak.get("start_time");
                String endTime = (String) peak.get("end_time");
                Integer peakTraffic = (Integer) peak.get("peak_traffic");
                String intensity = (String) peak.get("intensity");

                if (startTime != null && endTime != null) {
                    String displayStart = startTime.length() > 16 ? startTime.substring(11, 16) : startTime;
                    String displayEnd = endTime.length() > 16 ? endTime.substring(11, 16) : endTime;
                    result.append(String.format("🔥 %s-%s: %d人 (%s)\n",
                            displayStart, displayEnd, peakTraffic, intensity));
                }
            }
        }

        // 添加建议
        result.append("\n💡 建议:\n");
        if (peakPeriods != null && !peakPeriods.isEmpty()) {
            result.append("- 避开高峰时段可减少等待时间\n");
            result.append("- 建议在非高峰时段用餐\n");
        } else {
            result.append("- 预测期间人流相对平稳\n");
            result.append("- 各时段用餐体验较好\n");
        }

        return result.toString();
    }
}