package com.example.springdemo.logic;

import com.example.springdemo.pojo.User;
import com.example.springdemo.pojo.dto.LoginDto;
import com.example.springdemo.pojo.dto.RegisterDto;
import com.example.springdemo.pojo.dto.UserDto;
import com.example.springdemo.pojo.Record;
import com.example.springdemo.pojo.Reserve;

import java.util.Optional;

public interface IUserLogic {
    /**
     * add user
     * @param user
     */
    User add(UserDto user);
    /**
     * find username
     * @param userName
     */
    Optional <User> getUserName(String userName);
    /**
     * edit user
     * @param user
     */
    User edit(UserDto user);

    /**
     * delete user
     * @param userName
     */
    void delete(String userName);
    /**
     * register
     * @param dto
     */
    User register(RegisterDto dto);
    /**
     * login
     * @param dto
     */
    User login(LoginDto dto);

    void changePassword(String username, String oldPassword, String newPassword);

    void deleteUser(String username);
    
    // ===== 逻辑层功能接口 =====

    /**
     * 顾客预约排队
     * @param username 顾客用户名
     * @param restaurantId 餐厅编号
     * @param people 预约人数
     * @return 预约成功的记录
     */
    Reserve makeReservation(String username, int restaurantId, int people);

    /**
     * 取消顾客预约
     * @param username 顾客用户名
     * @param reserveId 预约记录编号
     */
    void cancelReservation(String username, int reserveId);

    /**
     * 查看餐厅当前状态（当前人数 + 已预约人数）
     * 仅顾客和经理可查看
     * @param username 用户名
     * @param restaurantId 餐厅编号
     * @return 最新餐厅记录
     */
    Record getRestaurantInfo(String username, int restaurantId);

    /**
     * 查看我的预约记录
     * @param username 顾客用户名
     * @return 该顾客所有预约记录
     */
    List<Reserve> getMyReservations(String username);

    /**
     * 顾客确认到达
     * @param username 顾客用户名
     * @param restaurantId 餐厅编号
     */
    void confirmArrival(String username, int reserveId);


}
