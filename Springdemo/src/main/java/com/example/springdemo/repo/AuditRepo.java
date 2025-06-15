package com.example.springdemo.repo;

import com.example.springdemo.pojo.User;
import com.example.springdemo.pojo.User_Audit;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AuditRepo extends CrudRepository<User_Audit, Integer> {

    @Query("SELECT u FROM User_Audit u WHERE u.applicant.id = :id")
    List<User_Audit> findByApplicantUserId(@Param("id") int id);
}
