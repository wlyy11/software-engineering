package com.example.springdemo.pojo.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import org.hibernate.validator.constraints.Length;

public class RegisterDto {
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
        return "RegisterDto{" +
                "name='" + name + '\'' +
                ", password='" + password + '\'' +
                ", authority='" + authority + '\'' +
                '}';
    }

    public void setName(@NotBlank(message = "用户名不能为空") @NotEmpty @NotNull String name) {
        this.name = name;
    }

    public void setPassword(@Length(min = 6, max = 20, message = "密码长度必须为6-20位") String password) {
        this.password = password;
    }

    public void setAuthority(@NotBlank(message = "权限不能为空") String authority) {
        this.authority = authority;
    }

    public @NotBlank(message = "用户名不能为空") @NotEmpty @NotNull String getName() {
        return name;
    }

    public @Length(min = 6, max = 20, message = "密码长度必须为6-20位") String getPassword() {
        return password;
    }

    public @NotBlank(message = "权限不能为空") String getAuthority() {
        return authority;
    }
}
