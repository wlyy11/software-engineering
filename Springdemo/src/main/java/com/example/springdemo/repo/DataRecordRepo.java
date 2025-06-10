package com.example.springdemo.repo;

import com.example.springdemo.pojo.DataRecord;
import org.springframework.data.jpa.repository.JpaRepository;

public interface DataRecordRepo extends JpaRepository<DataRecord, Long> {
}

