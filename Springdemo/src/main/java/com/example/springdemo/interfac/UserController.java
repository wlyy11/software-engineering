package com.example.springdemo.interfac;

import com.example.springdemo.logic.DataRecordService;
import org.springframework.ui.Model;
import org.springframework.stereotype.Controller;
import com.example.springdemo.logic.IUserLogic;
import com.example.springdemo.logic.TxtFileReader;
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

import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

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

        return "user"; // 显示 user.html
    }
    /*
    @GetMapping("/{userName}")  //URL:localhost:8080/user/name    method:get
    public ResponseMessage<User> findUserName(@PathVariable String userName) {
        User newUser = userLogic.getUserName(userName).
                orElseThrow(() -> new RuntimeException("用户不存在!"));
        return ResponseMessage.success(newUser);
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


    // register
    // 返回注册页面（GET）
    @GetMapping("/register")
    public String showRegisterPage() {
        return "register"; // 对应templates/register.html
    }

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

    @GetMapping("/login")
    public String showLoginPage() {
        System.out.println("!!!");
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

        UsernamePasswordAuthenticationToken auth = new UsernamePasswordAuthenticationToken(
                userDetails, null, userDetails.getAuthorities());
        SecurityContextHolder.getContext().setAuthentication(auth);
        System.out.println("currentUsername = " + SecurityContextHolder.getContext().getAuthentication().getName());
        return ResponseMessage.success(response);
    }

    // 查看自己信息
    @GetMapping("/me")
    public ResponseMessage<?> viewUser() {

        String currentUsername = SecurityContextHolder.getContext().getAuthentication().getName();
        System.out.println("Current username: " + currentUsername);
        User newUser = userLogic.getUserName(currentUsername)
                .orElseThrow(() -> new RuntimeException("用户不存在!"));
        return ResponseMessage.success(newUser);
    }

    // 修改密码
    @GetMapping("/change-password")
    public String showChangeWordPage(@RequestParam String username, Model model) {
    	model.addAttribute("username", username);
    	return "change-password";
    }

    @PutMapping("/change-password")
    public ResponseMessage<?> changePassword(@RequestBody ChangePasswordRequest request,
                                             @RequestParam String currentUsername) {

        System.out.println("currentUsername = " + currentUsername);
        System.out.println("requestUsername = " + request.getUsername());
        
        if (!currentUsername.equals(request.getUsername())) {
            throw new SecurityException("You can only change your own password");
        }
        userLogic.changePassword(request.getUsername(), request.getOldPassword(), request.getNewPassword());
        return ResponseMessage.success("Password changed successfully");
    }

    @DeleteMapping("/delete-user")
    public ResponseEntity<?> deleteAccount(@RequestBody DeleteUserRequest request,
                                           @RequestParam String currentUsername) {
        //String currentUsername = SecurityContextHolder.getContext().getAuthentication().getName();

        // 确保用户只能注销自己的账号
        if (!currentUsername.equals(request.getUsername())) {
            throw new SecurityException("You can only delete your own account");
        }

        // 验证密码
        userLogic.changePassword(request.getUsername(), request.getPassword(), request.getPassword());
        userLogic.deleteUser(request.getUsername());
        return ResponseEntity.ok("Account deleted successfully");
    }

    // 运行python
    @Autowired
    private PythonRunnerService pythonRunner;

    @GetMapping("/hello")
    public String hello(@RequestParam(required = false) String name) {
        return pythonRunner.runPythonScript(name);
    }

    // 读取txt文件
    @Autowired
    private TxtFileReader txtFileReader;
    @Autowired
    private DataRecordService DataRecordLogit;

    @GetMapping("/txt")
    public ResponseMessage<?> getAllTxtFiles() {
        try {
            String folderPath = "C:\\JAVA\\1\\Springdemo\\result_yolov5\\exp3";
            Map<String, String> s = txtFileReader.readAllTxtFiles(folderPath);
            System.out.println(s);
            DataRecordLogit.saveMapData(s);
            return ResponseMessage.success("success");

        } catch (IOException e) {
            throw new RuntimeException("错误!");
        }
    }

}
