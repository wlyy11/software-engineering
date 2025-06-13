package com.example.springdemo.pojo;

import jakarta.persistence.*;
import org.springframework.security.core.GrantedAuthority;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.stream.Collectors;
import org.springframework.security.core.authority.SimpleGrantedAuthority;

@Table(name = "tb_user")
@Entity

public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "user_id" )
    private Integer id;
    @Column(name = "user_name" )
    private String name;
    @Column(name = "user_password" )
    private String password;
    @Column(name = "user_authority" )
    private String authority;

    public enum UserStatus {
        PENDING,    // 待审核
        APPROVED,   // 已批准
        REJECTED    // 已拒绝
    }
    @Enumerated(EnumType.STRING)
    private UserStatus status = UserStatus.APPROVED; // 默认待审核状态



    private Collection<? extends GrantedAuthority> authorities;

    // 将字符串权限转换为 GrantedAuthority 集合
    private Collection<GrantedAuthority> convertAuthority(String authority) {
        if (authority == null || authority.isEmpty()) {
            return Collections.emptyList();
        }

        return Arrays.stream(authority.split(","))
                .map(String::trim)
                .map(SimpleGrantedAuthority::new)
                .collect(Collectors.toList());
    }

    public Collection<? extends GrantedAuthority> getAuthorities() {
        if (this.authorities == null) {
            this.authorities = convertAuthority(this.authority);
        }
        return authorities;
    }

    public User(){
        this.authorities = new ArrayList<>();
    }

    public User(Integer id, String name, String password, String authority) {
        this.id = id;
        this.name = name;
        this.password = password;
        this.authority = authority;
        this.authorities = convertAuthority(authority);
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setAuthority(String authority) {
        this.authority = authority;
    }

    public String getPassword() {
        return password;
    }

    public Integer getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getAuthority() {
        return authority;
    }

    public void setStatus(UserStatus status) {
        this.status = status;
    }

    public UserStatus getStatus() {
        return status;
    }

    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", password='" + password + '\'' +
                ", authority='" + authority + '\'' +
                '}';
    }
}
