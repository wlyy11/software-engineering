package com.example.springdemo.repo;

import com.example.springdemo.pojo.Appointment;
import com.example.springdemo.pojo.DataRecord;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface AppointRepo extends CrudRepository<Appointment, Integer> {

    @Query("SELECT COUNT(d) FROM Appointment d WHERE d.status ='WAITING' ")
    int findnumAppoint();

    @Query("SELECT d FROM Appointment d WHERE d.status ='WAITING' and d.restaurant.managerId = :id ")
    List<Appointment> findALLAppoint(@Param("id") int id);

    @Query("SELECT d FROM Appointment d WHERE d.user.id = :user_id ")
    List<Appointment> findUserAppoint(@Param("user_id") int user_id);
}
