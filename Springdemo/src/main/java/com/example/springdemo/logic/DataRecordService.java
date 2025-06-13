package com.example.springdemo.logic;

import com.example.springdemo.pojo.DataRecord;
import com.example.springdemo.repo.DataRecordRepo;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.stream.Collectors;

@Service
public class DataRecordService {

    private final DataRecordRepo repository;

    public DataRecordService(DataRecordRepo repository) {
        this.repository = repository;
    }

    @Transactional
    public void saveMapData(Map<String, String> dataMap) {
        List<DataRecord> records = dataMap.entrySet().stream()
                .sorted(Map.Entry.comparingByKey())
                .map(entry -> {
                    DataRecord record = new DataRecord();
                    record.setTime(entry.getKey());
                    record.setPerson(Integer.parseInt(entry.getValue()));
                    record.setRes_id(2);
                    return record;
                }).collect(Collectors.toList());

        repository.saveAll(records);

    }
}