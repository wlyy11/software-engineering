package com.example.springdemo.interfac;

import com.example.springdemo.logic.RegisterRequestLogic;
import com.example.springdemo.pojo.ResponseMessage;
import com.example.springdemo.pojo.User_Audit;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/user/admin")  //URL:localhost:8080/admin
@PreAuthorize("hasRole('ADMIN')")

public class AdminApprovalController {

    @Autowired
    private RegisterRequestLogic approvalService;

    // 获取待审核请求
    @GetMapping("/approvals/pending")
    public List<User_Audit> getPendingRequests() {

        String currentUsername = SecurityContextHolder.getContext().getAuthentication().getName();
        if (!currentUsername.equals("sa")) {
            throw new SecurityException("You are not sa!");
        }

        return approvalService.getPendingRequests();
    }


    // 处理审核请求
    @PostMapping("/approvals/{requestId}/handle")
    public ResponseMessage<?>  handleRequest(
            @PathVariable Integer requestId,
            @RequestParam boolean approved,
            @RequestParam(required = false) String comment) {

        String currentUsername = SecurityContextHolder.getContext().getAuthentication().getName();
        if (!currentUsername.equals("sa")) {
            throw new SecurityException("You are not sa!");
        }

        approvalService.handleRequest(requestId, approved, comment);
        return ResponseMessage.success("Successfully modified");
    }
}
