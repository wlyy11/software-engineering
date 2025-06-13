package com.example.springdemo.logic;

import com.example.springdemo.pojo.User;
import com.example.springdemo.pojo.dto.LoginDto;
import com.example.springdemo.pojo.dto.RegisterDto;
import com.example.springdemo.pojo.dto.UserDto;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;

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

}
