package com.example.springdemo.interfac;

import com.example.springdemo.logic.IUserLogic;
import org.springframework.ui.Model;
import org.springframework.stereotype.Controller;
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

@Controller
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
    @GetMapping("/{username}")
    public String showUserProfile(@PathVariable String username, Model model) {
        User user = userLogic.getUserName(username)
                .orElseThrow(() -> new RuntimeException("用户不存在"));

        model.addAttribute("username", user.getName());
        model.addAttribute("role", user.getAuthority()); // 确保 User 实体中有 getRole()

        return "user"; // 显示 user-info.html
    }

    /*
    @GetMapping("/{userName}")  //URL:localhost:8080/user/name    method:get
    public String findUserName(@PathVariable String userName) {
        User newUser = userLogic.getUserName(userName).
                orElseThrow(() -> new RuntimeException("用户不存在!"));
        return "user";
    }
    */

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
    // 返回注册页面（GET）
    @GetMapping("/register")
    public String showRegisterPage() {
        return "register"; // 对应templates/register.html
    }
    
    @PostMapping("/register")
    public ResponseMessage<User> register(@Validated @RequestBody RegisterDto dto) {
    	System.out.println("注册数据: " + dto);
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

    @GetMapping("/login")
    public String showLoginPage() {
    	return "login";
    }
    
    // 这个方法用于处理登录，并在成功后跳转到用户个人页面
    @PostMapping("/login")
    @ResponseBody
    public ResponseMessage<User> login(@RequestBody Map<String, String> authenticationRequest) {
    	
    	// 在控制台输出接收到的用户名和密码
        System.out.println("接收到的登录信息：");
        System.out.println("用户名: " + authenticationRequest.get("username"));
        System.out.println("密码: " + authenticationRequest.get("password"));
        
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(authenticationRequest.get("username"),
                        authenticationRequest.get("password"))
        );

        final UserDetails userDetails = userDetailsService.loadUserByUsername(authenticationRequest.get("username"));
        final String jwt = jwtUtil.generateToken(userDetails);
        System.out.println("jwt = " + jwt);

        Map<String, String> response = new HashMap<>();
        response.put("token", jwt);
        return ResponseMessage.success(response);
    }
    
    /*
    @PostMapping("/login")
    public String handleLogin(@RequestParam String username, @RequestParam String password) {
        // 在控制台输出接收到的用户名和密码
        System.out.println("接收到的登录信息：");
        System.out.println("用户名: " + username);
        System.out.println("密码: " + password);

        // 通过用户名和密码进行身份验证
        try {
            authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(username, password)
            );
            final UserDetails userDetails = userDetailsService.loadUserByUsername(username);
            final String jwt = jwtUtil.generateToken(userDetails);

            // 登录成功，重定向到用户个人页面
            return "redirect:/user/" + username; // 重定向到用户的个人界面
        } catch (Exception e) {
            // 登录失败，返回错误信息
            System.out.println("登录失败: " + e.getMessage());
            return "login";  // 返回登录页面以便用户重试
        }
    }
    */
    
    @GetMapping("/change-password")
    public String showChangeWordPage(@RequestParam String username, Model model) {
    	model.addAttribute("username", username);
    	return "change-password";
    }
    // 修改密码
    @PutMapping("/change-password")
    public ResponseMessage<?> changePassword(@RequestBody ChangePasswordRequest request) {
        String currentUsername = "bob";// = SecurityContextHolder.getContext().getAuthentication().getName();
        System.out.println("currentUsername = " + currentUsername);
        System.out.println("requestUsername = " + request.getUsername());
        
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
