package com.example.springdemo.exception;

import com.example.springdemo.pojo.ResponseMessage;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandlerAdvice {

    Logger logger = LoggerFactory.getLogger(GlobalExceptionHandlerAdvice.class);

    @ExceptionHandler(Exception.class)
    public ResponseMessage handlerException(Exception e, HttpServletRequest request, HttpServletResponse response) {

        // 如果是测试端点，不拦截异常，重新抛出让控制器处理
        if (request.getRequestURI().contains("/api/test/")) {
            if (e instanceof RuntimeException) {
                throw (RuntimeException) e;
            } else {
                throw new RuntimeException(e);
            }
        }

        logger.error("全局异常处理器捕获异常:");
        logger.error("请求URL: " + request.getRequestURL());
        logger.error("请求方法: " + request.getMethod());
        logger.error("异常类型: " + e.getClass().getName());
        logger.error("异常消息: " + e.getMessage());
        logger.error("异常详情:", e);
        
        // 如果是队列预测相关的请求，返回更详细的错误信息
        if (request.getRequestURI().contains("/api/queue-prediction/")) {
            return new ResponseMessage(500, "队列预测服务错误: " + e.getMessage(), null);
        }
        
        return new ResponseMessage(500,"error",null);
    }

}
