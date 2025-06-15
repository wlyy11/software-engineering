package com.example.springdemo.logic;

import com.example.springdemo.pojo.DataRecord;
import com.example.springdemo.pojo.Restaurant;
import com.example.springdemo.repo.DataRecordRepo;
import com.example.springdemo.repo.RestaurantRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class DataRecordService {

    @Autowired
    private final DataRecordRepo repository;
    @Autowired
    private final RestaurantRepo restaurantRepo;

    public DataRecordService(DataRecordRepo repository, RestaurantRepo restaurantRepo) {
        this.repository = repository;
        this.restaurantRepo = restaurantRepo;
    }

    @Transactional
    public void saveMapData(Map<String, String> dataMap) {
        List<DataRecord> records = dataMap.entrySet().stream()
                .sorted(Map.Entry.comparingByKey())
                .map(entry -> {
                    DataRecord record = new DataRecord();
                    record.setTime(entry.getKey());
                    record.setPerson(Integer.parseInt(entry.getValue()));
                    record.setRes_id(6);
                    return record;
                }).collect(Collectors.toList());

        repository.saveAll(records);
    }

    // 查询最新时间的人数
    public Optional<DataRecord> getLatestNum(int res_id) {

        if (restaurantRepo.findById(res_id).isEmpty()) {
            throw new RuntimeException("餐厅不存在!");
        }
        else{
            System.out.println(res_id);
            return repository.findLatestRecord(res_id);
        }
    }

    // 经理查看最近10条人数记录
    public List<DataRecord> getNLatestNum(int num, String res_name,int user_id) {
        if (restaurantRepo.findByRestaurantname(res_name).isEmpty()) {
            throw new RuntimeException("餐厅不存在!");
        }
        else{
            Restaurant restau =  restaurantRepo.findByRestaurantname(res_name).get();
            if (restau.getManagerId()!=user_id){
                throw new RuntimeException("不能查看其他餐厅的信息！");
            }
            int res_id = restau.getId();System.out.println(res_id);
            return repository.findNRecord(num, res_id);
        }

    }

    // 经理查看特定时间人数
    public List<DataRecord> getNLatestDate(String date, String res_name, int user_id) {
        if (restaurantRepo.findByRestaurantname(res_name).isEmpty()) {
            throw new RuntimeException("餐厅不存在!");
        }
        else{
            Restaurant restau =  restaurantRepo.findByRestaurantname(res_name).get();
            if (restau.getManagerId()!=user_id){
                throw new RuntimeException("不能查看其他餐厅的信息！");
            }
            int res_id = restau.getId();System.out.println(res_id);
            return repository.findDateRecord(date, res_id);
        }
    }


}