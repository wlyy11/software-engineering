package com.example.springdemo.repo;

import com.example.springdemo.pojo.Restaurant;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface RestaurantRepo extends CrudRepository<Restaurant, Integer> {

    @Query("SELECT u FROM Restaurant u WHERE u.name = :name")
    Optional<Restaurant> findByRestaurantname(@Param("name") String name);

    List<Restaurant> findAll();

    @Query("SELECT u FROM Restaurant u WHERE u.managerId = :id")
    List<Restaurant> findowner(@Param("id")Integer id);
}
