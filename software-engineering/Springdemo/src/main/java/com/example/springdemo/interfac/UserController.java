package com.example.springdemo.interfac;

import com.example.springdemo.logic.IUserLogic;
import com.example.springdemo.pojo.ResponseMessage;
import com.example.springdemo.pojo.User;
import com.example.springdemo.pojo.dto.*;
import com.example.springdemo.security.JwtUtil;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AnonymousAuthenticationToken;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/user") // URL:localhost:8080/user

public class UserController {

    @Autowired
    IUserLogic userLogic;
    @Autowired
    private JwtUtil jwtUtil;
    // rest

    // add
    @PostMapping
    public ResponseMessage<User> addUser(@Validated @RequestBody UserDto user) {
        User newUser = userLogic.add(user);

        return ResponseMessage.success(newUser);
    }

    // find
    @GetMapping("/{userName}")  //URL:localhost:8080/user/name    method:get
    public ResponseMessage<User> findUserName(@PathVariable String userName) {
        User newUser = userLogic.getUserName(userName).
                orElseThrow(() -> new RuntimeException("用户不存在!"));
        return ResponseMessage.success(newUser);
    }

    // change
    @PutMapping
    public ResponseMessage<User> edit(@Validated @RequestBody UserDto user) {
        User newUser = userLogic.edit(user);
        return ResponseMessage.success(newUser);
    }

    // delete
    @DeleteMapping("/{userName}")
    public ResponseMessage<User> delete(@PathVariable String userName) {
        userLogic.delete(userName);
        return ResponseMessage.success();
    }
    // register


    @PostMapping("/register")
    public ResponseMessage<User> register(@Validated @RequestBody RegisterDto dto) {

        User newUser = userLogic.register(dto);
        return ResponseMessage.success(newUser);
    }
    // login
    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private UserDetailsService userDetailsService;

    @PostMapping("/login")
    public ResponseMessage<User> login(@RequestBody Map<String, String> authenticationRequest) {

        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(authenticationRequest.get("username"),
                        authenticationRequest.get("password"))
        );

        final UserDetails userDetails = userDetailsService.loadUserByUsername(authenticationRequest.get("username"));
        final String jwt = jwtUtil.generateToken(userDetails);


        Map<String, String> response = new HashMap<>();
        response.put("token", jwt);
        return ResponseMessage.success(response);
    }

    // 修改密码
    @PutMapping("/change-password")
    public ResponseMessage<?> changePassword(@RequestBody ChangePasswordRequest request) {

        String currentUsername = SecurityContextHolder.getContext().getAuthentication().getName();
        System.out.println(currentUsername);

        if (!currentUsername.equals(request.getUsername())) {
            throw new SecurityException("You can only change your own password");
        }
        userLogic.changePassword(request.getUsername(), request.getOldPassword(), request.getNewPassword());
        return ResponseMessage.success("Password changed successfully");
    }

    @DeleteMapping("/delete-user")
    public ResponseEntity<?> deleteAccount(@RequestBody DeleteUserRequest request) {
        String currentUsername = SecurityContextHolder.getContext().getAuthentication().getName();

        // 确保用户只能注销自己的账号
        if (!currentUsername.equals(request.getUsername())) {
            throw new SecurityException("You can only delete your own account");
        }

        // 验证密码
        userLogic.changePassword(request.getUsername(), request.getPassword(), request.getPassword());
        userLogic.deleteUser(request.getUsername());
        return ResponseEntity.ok("Account deleted successfully");
    }

}
