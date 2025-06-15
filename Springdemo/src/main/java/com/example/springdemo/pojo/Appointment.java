package com.example.springdemo.pojo;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.persistence.*;

@Table(name = "tb_appoint")
@Entity
public class Appointment {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "appoint_id")
    private int id;

    @ManyToOne(cascade = CascadeType.PERSIST)
    @JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})
    private User user; // 顾客id

    @ManyToOne(cascade = CascadeType.PERSIST)
    @JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})
    private Restaurant restaurant; // 餐厅编号

    @Column(name = "appoint_time")
    private String time; // 预约时间（字符串或时间戳）

    public enum AppointStatus {
        WAITING,    // 等待
        COMPLETED   // 完成
    }
    @Enumerated(EnumType.STRING)
    private AppointStatus status = AppointStatus.WAITING;

    public Appointment() {}

    @Override
    public String toString() {
        return "Appointment{" +
                "id=" + id +
                ", user=" + user +
                ", restaurant=" + restaurant +
                ", time='" + time + '\'' +
                ", status=" + status +
                '}';
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public Restaurant getRestaurant() {
        return restaurant;
    }

    public void setRestaurant(Restaurant restaurant) {
        this.restaurant = restaurant;
    }

    public String getTime() {
        return time;
    }

    public void setTime(String time) {
        this.time = time;
    }

    public AppointStatus getStatus() {
        return status;
    }

    public void setStatus(AppointStatus status) {
        this.status = status;
    }

    public Appointment(int id, User user, Restaurant restaurant, String time, AppointStatus status) {
        this.id = id;
        this.user = user;
        this.restaurant = restaurant;
        this.time = time;
        this.status = status;
    }
}