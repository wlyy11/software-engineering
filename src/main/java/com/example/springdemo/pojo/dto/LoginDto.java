package com.example.springdemo.pojo.dto;

public class LoginDto {
    private String name;
    private String password;

    @Override
    public String toString() {
        return "LoginDto{" +
                "username='" + name + '\'' +
                ", password='" + password + '\'' +
                '}';
    }

    public void setName(String username) {
        this.name = username;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getName() {
        return name;
    }

    public String getPassword() {
        return password;
    }
}
