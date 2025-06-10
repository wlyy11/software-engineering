package com.example.springdemo.pojo.dto;

public class DeleteUserRequest {
    private String username;
    private String password;

    @Override
    public String toString() {
        return "DeleteUserRequest{" +
                "username='" + username + '\'' +
                ", password='" + password + '\'' +
                '}';
    }

    public DeleteUserRequest(String password, String username) {
        this.password = password;
        this.username = username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getUsername() {
        return username;
    }

    public String getPassword() {
        return password;
    }
}
