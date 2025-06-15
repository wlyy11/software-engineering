package com.example.springdemo.interfac;


import com.example.springdemo.logic.DataRecordService;
import com.example.springdemo.logic.IUserLogic;
import com.example.springdemo.pojo.DataRecord;
import com.example.springdemo.pojo.ResponseMessage;
import com.example.springdemo.pojo.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
@RequestMapping("/user") // URL:localhost:8080/user
public class RecordController {

    @Autowired
    DataRecordService recordService;
    @Autowired
    IUserLogic userLogic;

    // 顾客查看人数
    @GetMapping("/appointment/record")
    @ResponseBody
    public ResponseMessage<?> viewUser(@RequestParam int res_id,
                                       @RequestParam String currentUsername) {

        //String currentUsername = SecurityContextHolder.getContext().getAuthentication().getName();
        System.out.println("Current username: " + currentUsername);
        System.out.println("res_id: " + res_id);

        User newUser = userLogic.getUserName(currentUsername)
                .orElseThrow(() -> new RuntimeException("用户不存在!"));

        if (recordService.getLatestNum(res_id).isEmpty()) {
            return ResponseMessage.success("暂无记录！");
        }
        else {
            DataRecord nowrecord =  recordService.getLatestNum(res_id).get();
            return ResponseMessage.success(nowrecord.getPerson(),nowrecord.getTime());
        }

    }

    // 经理查看最近10次人数
    @GetMapping("/record_viewManager")
    @ResponseBody
    public ResponseMessage<?> viewManager(@RequestParam(defaultValue = "10") int count,
                                          @RequestParam String res_name,
                                          @RequestParam String currentUsername) {

        //String currentUsername = SecurityContextHolder.getContext().getAuthentication().getName();
        System.out.println("Current username: " + currentUsername);

        User newUser = userLogic.getUserName(currentUsername)
                .orElseThrow(() -> new RuntimeException("用户不存在!"));

        if (!Objects.equals(newUser.getAuthority(), "经理")) {
            throw new RuntimeException("权限不足！");
        }

        List<DataRecord> nowrecord =  recordService.getNLatestNum(count,res_name,newUser.getId());

        Map<String, Integer> result = new LinkedHashMap<>();
        for (DataRecord record : nowrecord) {
            result.put(record.getTime(), record.getPerson());
        }

        List<Map.Entry<String, Integer>> entryList = new ArrayList<>(result.entrySet());
        ListIterator<Map.Entry<String, Integer>> iterator = entryList.listIterator(entryList.size());

        Map<String, Integer> reversedMap = new LinkedHashMap<>();
        while (iterator.hasPrevious()) {
            Map.Entry<String, Integer> entry = iterator.previous();
            reversedMap.put(entry.getKey(), entry.getValue());
        }

        System.out.println(reversedMap);

        return ResponseMessage.success(reversedMap);
    }

    // 经理查看特定时间人数
    @GetMapping("/record_viewDate")
    @ResponseBody
    public ResponseMessage<?> viewManagerDate(@RequestParam(defaultValue = "6_09") String date,
                                              @RequestParam String res_name,
                                              @RequestParam String currentUsername) {

        //String currentUsername = SecurityContextHolder.getContext().getAuthentication().getName();
        System.out.println("Current username: " + currentUsername);

        User newUser = userLogic.getUserName(currentUsername)
                .orElseThrow(() -> new RuntimeException("用户不存在!"));

        if (!Objects.equals(newUser.getAuthority(), "经理")) {
            throw new RuntimeException("权限不足！");
        }

        List<DataRecord> nowrecord =  recordService.getNLatestDate(date,res_name,newUser.getId());

        Map<String, Integer> result = new LinkedHashMap<>();
        for (DataRecord record : nowrecord) {
            result.put(record.getTime(), record.getPerson());
        }

        List<Map.Entry<String, Integer>> entryList = new ArrayList<>(result.entrySet());
        ListIterator<Map.Entry<String, Integer>> iterator = entryList.listIterator(entryList.size());

        Map<String, Integer> reversedMap = new LinkedHashMap<>();
        while (iterator.hasPrevious()) {
            Map.Entry<String, Integer> entry = iterator.previous();
            reversedMap.put(entry.getKey(), entry.getValue());
        }

        System.out.println(reversedMap);

        //String chartHtml = recordService.generateLineChart(result);

        return ResponseMessage.success(reversedMap);
    }

}
