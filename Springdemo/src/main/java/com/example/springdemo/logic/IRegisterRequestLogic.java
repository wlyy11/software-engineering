package com.example.springdemo.logic;

import com.example.springdemo.pojo.User_Audit;

import java.util.List;

public interface IRegisterRequestLogic {

    /**
     * 获取待审核请求
     */
    List<User_Audit> getPendingRequests();
    /**
     * 处理审核请求
     * @param requestId,approved,comment
     */
    void handleRequest(Integer requestId, boolean approved, String comment);
}
