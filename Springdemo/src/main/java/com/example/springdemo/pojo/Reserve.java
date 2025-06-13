package com.example.springdemo.pojo;

import jakarta.persistence.*;

@Table(name = "tb_reserve")
@Entity
public class Reserve {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "reserve_id")
    private int id;

    @Column(name = "reserve_user")
    private String username; // 顾客用户名

    @Column(name = "reserve_time")
    private String time; // 预约时间（字符串或时间戳）

    @Column(name = "reserve_restaurant_id")
    private int restaurantId; // 餐厅编号

    public Reserve() {}

    public Reserve(int id, String username, String time, int restaurantId) {
        this.id = id;
        this.username = username;
        this.time = time;
        this.restaurantId = restaurantId;
    }

    public int getId() {
        return id;
    }

    public String getUsername() {
        return username;
    }


    public String getTime() {
        return time;
    }

    public int getRestaurantId() {
        return restaurantId;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setUsername(String username) {
        this.username = username;
    }


    public void setTime(String time) {
        this.time = time;
    }

    public void setRestaurantId(int restaurantId) {
        this.restaurantId = restaurantId;
    }

    @Override
    public String toString() {
        return "Reserve{" +
                "id=" + id +
                ", username='" + username + '\'' +
                ", time='" + time + '\'' +
                ", restaurantId=" + restaurantId +
                '}';
    }
}
