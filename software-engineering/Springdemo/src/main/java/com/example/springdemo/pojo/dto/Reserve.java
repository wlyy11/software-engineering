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

    @Column(name = "reserve_people")
    private int people; // 预约人数

    @Column(name = "reserve_time")
    private String time; // 预约提交时间（记录）

    @Column(name = "reserve_arrival_estimate")
    private String arrivalEstimate; // 顾客预计到达时间

    @Column(name = "reserve_restaurant_id")
    private int restaurantId; // 餐厅编号

    public Reserve() {}

    public Reserve(int id, String username, int people, String time, String arrivalEstimate, int restaurantId) {
        this.id = id;
        this.username = username;
        this.people = people;
        this.time = time;
        this.arrivalEstimate = arrivalEstimate;
        this.restaurantId = restaurantId;
    }

    // Getters
    public int getId() {
        return id;
    }

    public String getUsername() {
        return username;
    }

    public int getPeople() {
        return people;
    }

    public String getTime() {
        return time;
    }

    public String getArrivalEstimate() {
        return arrivalEstimate;
    }

    public int getRestaurantId() {
        return restaurantId;
    }

    // Setters
    public void setId(int id) {
        this.id = id;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public void setPeople(int people) {
        this.people = people;
    }

    public void setTime(String time) {
        this.time = time;
    }

    public void setArrivalEstimate(String arrivalEstimate) {
        this.arrivalEstimate = arrivalEstimate;
    }

    public void setRestaurantId(int restaurantId) {
        this.restaurantId = restaurantId;
    }

    @Override
    public String toString() {
        return "Reserve{" +
                "id=" + id +
                ", username='" + username + '\'' +
                ", people=" + people +
                ", time='" + time + '\'' +
                ", arrivalEstimate='" + arrivalEstimate + '\'' +
                ", restaurantId=" + restaurantId +
                '}';
    }
}
