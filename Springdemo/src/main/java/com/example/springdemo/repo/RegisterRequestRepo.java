package com.example.springdemo.repo;

import com.example.springdemo.pojo.User;
import com.example.springdemo.pojo.User_Audit;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface RegisterRequestRepo extends CrudRepository<User_Audit, Integer> {

    @Query("SELECT u FROM User_Audit u WHERE u.audit_id = :id")
    Optional<User_Audit> findById(@Param("id") Integer id);

    List<User_Audit> findByHandledFalse();
}
