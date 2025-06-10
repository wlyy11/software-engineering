package com.example.springdemo.security;

import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;

import javax.crypto.SecretKey;
import java.util.Base64;

public class Key {
    public static void main(String[] args) {
        // 生成安全的HS512密钥
        SecretKey key = Keys.secretKeyFor(SignatureAlgorithm.HS512);

        // 转换为Base64字符串
        String base64Key = Base64.getEncoder().encodeToString(key.getEncoded());

        System.out.println("安全的JWT密钥: " + base64Key);
        System.out.println("密钥长度: " + (base64Key.length() * 6 / 8) + "位"); // 验证长度
    }
}
