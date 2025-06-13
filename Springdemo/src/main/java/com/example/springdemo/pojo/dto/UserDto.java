package com.example.springdemo.pojo.dto;

import jakarta.persistence.Column;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import org.hibernate.validator.constraints.Length;

public class UserDto {

    private Integer id;
    @NotBlank(message = "用户名不能为空")
    @NotEmpty
    @NotNull
    private String name;
    @Length(min = 6, max = 20, message = "密码长度必须为6-20位")
    private String password;
    @NotBlank(message = "权限不能为空")
    private String authority;

    @Override
    public String toString() {
        return "UserDto{" +
                "authority='" + authority + '\'' +
                ", password='" + password + '\'' +
                ", name='" + name + '\'' +
                '}';
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getId() {
        return id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public void setAuthority(String authority) {
        this.authority = authority;
    }

    public String getName() {
        return name;
    }

    public String getPassword() {
        return password;
    }

    public String getAuthority() {
        return authority;
    }
}

