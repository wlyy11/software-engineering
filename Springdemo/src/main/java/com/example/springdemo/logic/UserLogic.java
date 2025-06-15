package com.example.springdemo.logic;

import com.example.springdemo.pojo.User;
import com.example.springdemo.pojo.User_Audit;
import com.example.springdemo.pojo.dto.LoginDto;
import com.example.springdemo.pojo.dto.RegisterDto;
import com.example.springdemo.pojo.dto.UserDto;
import com.example.springdemo.repo.AuditRepo;
import com.example.springdemo.repo.RegisterRequestRepo;
import com.example.springdemo.repo.UserRepo;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;


import java.util.*;
import java.util.stream.Collectors;

import static com.example.springdemo.pojo.User.UserStatus.*;

@Service // spring的bean

public class UserLogic implements IUserLogic {

    @Autowired
    UserRepo userRepo;
    @Autowired
    private RegisterRequestRepo requestRepo;
    @Autowired
    private AuditRepo auditRepository;


    @Override
    public User add(UserDto user) {

        User newUser = new User();
        BeanUtils.copyProperties(user,newUser);
        if (userRepo.findByUsername(newUser.getName()).isPresent()) {
            throw new RuntimeException("用户已存在，请重新输入用户名!");
        }
        else {
            return userRepo.save(newUser);   // 增加与修改 自动判别user是否有id，有就是修改，反之增加
        }
    }

    @Override
    public Optional <User> getUserName(String userName) {

        return userRepo.findByUsername(userName);
    }

    @Override
    public User edit(UserDto user) {
        User newUser = new User();
        BeanUtils.copyProperties(user,newUser);
        return userRepo.save(newUser);
    }

    @Override
    public void delete(String userName) {

        if (userRepo.findByUsername(userName).isEmpty()) {
            throw new RuntimeException("用户不存在，请重新输入用户名!");
        }
        else {
            userRepo.deleteById(userRepo.findByUsername(userName).get().getId());
        }
    }

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Override
    public User register(RegisterDto user) {

        if (userRepo.findByUsername(user.getName()).isPresent()) {
            throw new RuntimeException("用户已存在，请重新输入用户名!");
        }
        else{
            user.setPassword(passwordEncoder.encode(user.getPassword()));
            User newUser = new User();
            BeanUtils.copyProperties(user,newUser);

            if (Objects.equals(newUser.getAuthority(),"经理")){
                newUser.setStatus(PENDING);

                // 创建审核请求
                User_Audit request = new User_Audit();
                request.setApplicant(newUser);
                requestRepo.save(request);

                return userRepo.save(newUser);
            }
            else if (Objects.equals(newUser.getAuthority(),"管理员")){
                newUser.setStatus(REJECTED);
                return userRepo.save(newUser);
            }
            else {
                newUser.setStatus(APPROVED);
                return userRepo.save(newUser);
            }

        }
    }

    @Override
    public User login(LoginDto user) {

        if (userRepo.findByUsername(user.getName()).isEmpty()) {
            System.out.println(userRepo.findByUsername(user.getName()));
            throw new RuntimeException("用户不存在，请重新输入用户名!");
        }
        else {
            User newuser = userRepo.findByUsername(user.getName()).get();
            if (passwordEncoder.matches(user.getPassword(), newuser.getPassword())){
                return userRepo.findByUsername(user.getName()).get();
            }
            else {
                throw new RuntimeException("密码错误!");
            }
        }
    }

    @Override
        public void changePassword(String username, String oldPassword, String newPassword){

        User user = userRepo.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));

        if (!passwordEncoder.matches(oldPassword, user.getPassword())) {
            throw new RuntimeException("Invalid old password");
        }

        user.setPassword(passwordEncoder.encode(newPassword));
        userRepo.save(user);
    }

    @Override
    public  void deleteUser(String username){

        User user = userRepo.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));

        List<User_Audit> audits = auditRepository.findByApplicantUserId(user.getId());
        auditRepository.deleteAll(audits);

        userRepo.delete(user);
    }

}
