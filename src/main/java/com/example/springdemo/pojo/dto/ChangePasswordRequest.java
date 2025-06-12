package com.example.springdemo.pojo.dto;

public class ChangePasswordRequest {
    private String username;
    private String oldPassword;
    private String newPassword;

    public ChangePasswordRequest(String newPassword, String oldPassword, String username) {
        this.newPassword = newPassword;
        this.oldPassword = oldPassword;
        this.username = username;
    }

    @Override
    public String toString() {
        return "ChangePasswordRequest{" +
                "username='" + username + '\'' +
                ", oldPassword='" + oldPassword + '\'' +
                ", newPassword='" + newPassword + '\'' +
                '}';
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public void setOldPassword(String oldPassword) {
        this.oldPassword = oldPassword;
    }

    public void setNewPassword(String newPassword) {
        this.newPassword = newPassword;
    }

    public String getUsername() {
        return username;
    }

    public String getOldPassword() {
        return oldPassword;
    }

    public String getNewPassword() {
        return newPassword;
    }
}
