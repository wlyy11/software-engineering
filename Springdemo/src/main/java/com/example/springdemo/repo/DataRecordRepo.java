package com.example.springdemo.repo;

import com.example.springdemo.pojo.DataRecord;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface DataRecordRepo extends JpaRepository<DataRecord, Long> {

    @Query("SELECT d FROM DataRecord d WHERE d.res_id = :res_id ORDER BY d.time DESC LIMIT 1")
    Optional<DataRecord> findLatestRecord(@Param("res_id") int res_id);

    @Query("SELECT d FROM DataRecord d WHERE d.res_id = :res_id ORDER BY d.time DESC LIMIT :num")
    List<DataRecord> findNRecord(@Param("num") int num, @Param("res_id") int res_id);

    @Query("SELECT d FROM DataRecord d WHERE d.res_id = :res_id and d.time LIKE CONCAT(:date, '%') ORDER BY d.time DESC ")
    List<DataRecord> findDateRecord(@Param("date") String date, @Param("res_id") int res_id);



}

