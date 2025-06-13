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
    @Column(name = "restaurant_local" )
    private String local;
    @Column(name = "restaurant_maxCapacity" )
    private int maxCapacity;

    public Restaurant() {}
    public Restaurant(int id, String name, int managerId, int maxCapacity) {
        this.id = id;
        this.name = name;
        this.managerId = managerId;
        this.maxCapacity = maxCapacity;
    }

    @Override
    public String toString() {
        return "Restaurant{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", managerId=" + managerId +
                ", local='" + local + '\'' +
                ", maxCapacity=" + maxCapacity +
                '}';
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getManagerId() {
        return managerId;
    }

    public void setManagerId(int managerId) {
        this.managerId = managerId;
    }

    public String getLocal() {
        return local;
    }

    public void setLocal(String local) {
        this.local = local;
    }

    public int getMaxCapacity() {
        return maxCapacity;
    }

    public void setMaxCapacity(int maxCapacity) {
        this.maxCapacity = maxCapacity;
    }

    public Restaurant(int id, String name, int managerId, String local, int maxCapacity) {
        this.id = id;
        this.name = name;
        this.managerId = managerId;
        this.local = local;
        this.maxCapacity = maxCapacity;
    }
}
