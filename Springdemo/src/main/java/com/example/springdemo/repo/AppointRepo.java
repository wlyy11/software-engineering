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

    // 新增：查找用户的等待中预约（最早的一个）
    @Query("SELECT a FROM Appointment a WHERE a.user.id = :userId AND a.status = 'WAITING' ORDER BY a.time ASC LIMIT 1")
    Optional<Appointment> findUserWaitingAppointment(@Param("userId") int userId);

    // 新增：查找特定餐厅按预约时间排序的等待队列
    @Query("SELECT a FROM Appointment a WHERE a.restaurant.id = :restaurantId AND a.status = 'WAITING' ORDER BY a.time ASC")
    List<Appointment> findWaitingAppointmentsByRestaurantOrderByTime(@Param("restaurantId") int restaurantId);

    // 新增：查找特定餐厅的去重用户等待队列（按最早预约时间排序）
    @Query("SELECT a FROM Appointment a WHERE a.restaurant.id = :restaurantId AND a.status = 'WAITING' " +
            "AND a.time = (SELECT MIN(a2.time) FROM Appointment a2 WHERE a2.user.id = a.user.id AND a2.restaurant.id = :restaurantId AND a2.status = 'WAITING') " +
            "ORDER BY a.time ASC")
    List<Appointment> findUniqueWaitingUsersByRestaurant(@Param("restaurantId") int restaurantId);

    // 新增：统计特定餐厅的去重等待用户数量
    @Query("SELECT COUNT(DISTINCT a.user.id) FROM Appointment a WHERE a.restaurant.id = :restaurantId AND a.status = 'WAITING'")
    int countUniqueWaitingUsersByRestaurant(@Param("restaurantId") int restaurantId);
}
