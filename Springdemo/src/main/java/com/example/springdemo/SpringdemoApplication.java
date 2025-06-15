package com.example.springdemo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.http.MediaType;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;
import org.springframework.web.client.RestTemplate;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@SpringBootApplication
public class SpringdemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringdemoApplication.class, args);
    }

    @Bean
    public RestTemplate restTemplate() {
        RestTemplate restTemplate = new RestTemplate();

        // 创建Jackson消息转换器
        MappingJackson2HttpMessageConverter jsonConverter = new MappingJackson2HttpMessageConverter();
        jsonConverter.setSupportedMediaTypes(Arrays.asList(
                MediaType.APPLICATION_JSON,
                MediaType.APPLICATION_JSON_UTF8,
                MediaType.TEXT_PLAIN,
                new MediaType("application", "json", java.nio.charset.StandardCharsets.UTF_8)
        ));

        // 清空现有转换器，重新设置
        List<HttpMessageConverter<?>> messageConverters = new ArrayList<>();
        messageConverters.add(jsonConverter);
        messageConverters.addAll(restTemplate.getMessageConverters());

        restTemplate.setMessageConverters(messageConverters);
        return restTemplate;
    }

}
