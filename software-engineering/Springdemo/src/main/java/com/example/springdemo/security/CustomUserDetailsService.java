package com.example.springdemo.security;

import com.example.springdemo.pojo.User;
import com.example.springdemo.repo.UserRepo;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service // 关键注解：标记为 Spring Bean
public class CustomUserDetailsService implements UserDetailsService {

    // 假设已注入 UserRepository（根据实际数据源调整）
    private final UserRepo userRepository;

    public CustomUserDetailsService(UserRepo userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {

        User user = userRepository.findByUsername(username)
                .orElseThrow(() ->
                        new UsernameNotFoundException("User not found: " + username)
                );

        return org.springframework.security.core.userdetails.User
                .withUsername(user.getName())
                .password(user.getPassword()) // 数据库中的加密密码
                .authorities(user.getAuthorities()) // 设置权限
                .build();
    }
}
