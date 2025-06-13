package com.example.springdemo.logic;

import com.example.springdemo.pojo.User;
import com.example.springdemo.pojo.User_Audit;
import com.example.springdemo.repo.RegisterRequestRepo;
import com.example.springdemo.repo.UserRepo;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service // spring的bean
public class RegisterRequestLogic implements IRegisterRequestLogic {

    @Autowired
    private RegisterRequestRepo requestRepo;
    @Autowired
    private UserRepo userRepo;

    public List<User_Audit> getPendingRequests() {
        return requestRepo.findByHandledFalse();
    }

    public void handleRequest(Integer requestId, boolean approved, String comment) {

        User_Audit request = requestRepo.findById(requestId)
                .orElseThrow(() -> new EntityNotFoundException("请求不存在"));
        User applicant = request.getApplicant();
        if(approved){
            applicant.setStatus(User.UserStatus.APPROVED);
        }
        else {
            applicant.setStatus(User.UserStatus.REJECTED);
        }
        request.setHandled(true);
        userRepo.save(applicant);
        requestRepo.save(request);
    }
}
