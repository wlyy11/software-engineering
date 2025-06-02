package com.example.springdemo.pojo;

import jakarta.persistence.*;

@Table(name = "tb_restaurant")
@Entity
public class Restaurant {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "restaurant_id" )
    private int id;
    @Column(name = "restaurant_name" )
    private String name;
    @Column(name = "restaurant_managerId" )
    private int managerId;
    @Column(name = "restaurant_maxCapacity" )
    private int maxCapacity;

    public Restaurant() {}
    public Restaurant(int id, String name, int managerId, int maxCapacity) {
        this.id = id;
        this.name = name;
        this.managerId = managerId;
        this.maxCapacity = maxCapacity;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setManagerId(int managerId) {
        this.managerId = managerId;
    }

    public void setMaxCapacity(int maxCapacity) {
        this.maxCapacity = maxCapacity;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public int getManagerId() {
        return managerId;
    }

    public int getMaxCapacity() {
        return maxCapacity;
    }

    @Override
    public String toString() {
        return "restaurant{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", managerId=" + managerId +
                ", maxCapacity=" + maxCapacity +
                '}';
    }
}
