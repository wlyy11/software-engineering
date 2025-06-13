package com.example.springdemo.repo;

import com.example.springdemo.pojo.User;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository   // Spring bean
public interface UserRepo extends CrudRepository<User, Integer> {

    @Query("SELECT u FROM User u WHERE u.name = :name")
    Optional <User> findByUsername(@Param("name") String name);


}
