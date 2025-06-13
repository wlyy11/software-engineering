package com.example.springdemo.pojo.dto;

import jakarta.validation.constraints.*;
import org.hibernate.validator.constraints.Length;

public class RestaurantDto {

    private Integer id;
    @NotBlank(message = "用户名不能为空")
    @NotEmpty
    @NotNull
    private String restaurant_name;

    @NotBlank(message = "位置信息不能为空")
    private String local;

    @NotNull(message = "人数不能为空")
    @Min(value = 1, message = "至少需要1人")
    @Max(value = 500, message = "最多500人")
    private int maxCapacity;

    private int manager_id;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public @NotBlank(message = "用户名不能为空") @NotEmpty @NotNull String getRestaurant_name() {
        return restaurant_name;
    }

    public void setRestaurant_name(@NotBlank(message = "用户名不能为空") @NotEmpty @NotNull String restaurant_name) {
        this.restaurant_name = restaurant_name;
    }

    public @NotBlank(message = "位置信息不能为空") String getLocal() {
        return local;
    }

    public void setLocal(@NotBlank(message = "位置信息不能为空") String local) {
        this.local = local;
    }

    public @NotNull(message = "人数不能为空") @Min(value = 1, message = "至少需要1人") @Max(value = 500, message = "最多500人") int getMaxCapacity() {
        return maxCapacity;
    }

    public void setMaxCapacity(@NotNull(message = "人数不能为空") @Min(value = 1, message = "至少需要1人") @Max(value = 500, message = "最多500人") int maxCapacity) {
        this.maxCapacity = maxCapacity;
    }

    public int getManager_id() {
        return manager_id;
    }

    public void setManager_id(int manager_id) {
        this.manager_id = manager_id;
    }

    public RestaurantDto(Integer id, String restaurant_name, String local, int maxCapacity, int manager_id) {
        this.id = id;
        this.restaurant_name = restaurant_name;
        this.local = local;
        this.maxCapacity = maxCapacity;
        this.manager_id = manager_id;
    }
}
