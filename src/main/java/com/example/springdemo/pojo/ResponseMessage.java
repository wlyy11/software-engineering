package com.example.springdemo.pojo;

import org.springframework.http.HttpStatus;

import java.util.Collections;
import java.util.Map;
import java.util.stream.Collectors;

public class ResponseMessage<T> {

    private Integer code;
    private String message;
    private T data;

    public void setCode(Integer code) {
        this.code = code;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public void setData(T data) {
        this.data = data;
    }

    public Integer getCode() {
        return code;
    }

    public String getMessage() {
        return message;
    }

    public T getData() {
        return data;
    }

    public ResponseMessage(Integer code, String message, T data) {
        this.code = code;
        this.message = message;
        this.data = data;
    }

    public static <T> ResponseMessage<T> success(T data) {
        return new ResponseMessage(HttpStatus.OK.value(), "success", data);
    }
    public static <T> ResponseMessage<T> success() {
        return new ResponseMessage(HttpStatus.OK.value(), "success", null);
    }
    public static <T> ResponseMessage<T> success(String message) {
        return new ResponseMessage(HttpStatus.OK.value(), message, null);
    }
    public static <T> ResponseMessage<T> success(Map<String, String> message) {
        String result = message.entrySet().stream()
                .map(entry -> entry.getKey() + "=" + entry.getValue())
                .collect(Collectors.joining(", "));
        return new ResponseMessage(HttpStatus.OK.value(), result, null);
    }

    public static <T> ResponseMessage<T> success(int num,String time) {
        return new ResponseMessage(HttpStatus.OK.value(), time, num);
    }



}
