package com.example.springdemo.interfac;

import com.example.springdemo.logic.IUserLogic;
import com.example.springdemo.logic.RestuarantLogit;
import com.example.springdemo.pojo.ResponseMessage;
import com.example.springdemo.pojo.Restaurant;
import com.example.springdemo.pojo.User;
import com.example.springdemo.pojo.dto.RegisterDto;
import com.example.springdemo.pojo.dto.RestaurantDto;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Objects;

@RestController
@RequestMapping("/user") // URL:localhost:8080/user
public class RestaurantController {

    // 新建餐厅
    @Autowired
    IUserLogic userLogic;
    @Autowired
    RestuarantLogit restuarantLogit;

    @PostMapping("/New_Restaurant")
    public ResponseMessage<?> newRestaurant(@Validated @RequestBody RestaurantDto dto,
                                            @RequestParam String currentUsername,
                                            HttpServletRequest request) {

        System.out.println("Request URL: " + request.getRequestURL());
        System.out.println("Method: " + request.getMethod());

        User newUser = userLogic.getUserName(currentUsername)
                .orElseThrow(() -> new RuntimeException("用户不存在!"));

        if (!Objects.equals(newUser.getAuthority(), "经理")){
            throw new SecurityException("Insufficient permissions!");
        }

        dto.setManager_id(newUser.getId());
        System.out.println(dto);
        Restaurant newRestau = restuarantLogit.newRestau(dto);

        return ResponseMessage.success(newRestau);
    }

    // 查看所有餐厅，顾客
    @GetMapping("/viewRestaurant")
    public ResponseMessage<?> viewRestaurant(@RequestParam String currentUsername) {

        User newUser = userLogic.getUserName(currentUsername)
                .orElseThrow(() -> new RuntimeException("用户不存在!"));

        if(!Objects.equals(newUser.getAuthority(), "顾客")){
            throw new SecurityException("Insufficient permissions!");
        }

        List<Restaurant> newRestau = restuarantLogit.getAllRestaurants();

        return ResponseMessage.success(newRestau);
    }

    // 查看自己管理的餐厅，经理
    @GetMapping("/viewOwnerRestaurant")
    public ResponseMessage<?> viewOwnerRestaurant(@RequestParam String currentUsername) {

        User newUser = userLogic.getUserName(currentUsername)
                .orElseThrow(() -> new RuntimeException("用户不存在!"));

        if(!Objects.equals(newUser.getAuthority(), "经理")){
            throw new SecurityException("Insufficient permissions!");
        }

        System.out.println(newUser.getId());
        List<Restaurant> newRestau = restuarantLogit.getRestaurants(newUser.getId());

        return ResponseMessage.success(newRestau);
    }

    // delete
    @DeleteMapping("/deleteOwnerRestaurant")
    public ResponseMessage<User> deleteRestaurant(@RequestParam String currentUsername,
                                                  @RequestParam String restaurantname) {

        System.out.println(currentUsername);

        User newUser = userLogic.getUserName(currentUsername)
                .orElseThrow(() -> new RuntimeException("用户不存在!"));

        if(!Objects.equals(newUser.getAuthority(), "经理")){
            throw new SecurityException("Insufficient permissions!");
        }

        System.out.println(newUser.getId());
        restuarantLogit.deleterestaurant(newUser.getId(), restaurantname);

        return ResponseMessage.success("delete success!");

    }

}
