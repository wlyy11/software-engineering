package com.example.springdemo.logic;

import com.example.springdemo.pojo.Restaurant;
import com.example.springdemo.pojo.User;
import com.example.springdemo.pojo.dto.RestaurantDto;
import com.example.springdemo.repo.RestaurantRepo;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class RestuarantLogit {
    @Autowired
    RestaurantRepo restaurantRepo;


    public Optional<Restaurant> getRestaurantName(String restaurantName) {
        return restaurantRepo.findByRestaurantname(restaurantName);
    }

    public Restaurant newRestau(RestaurantDto dto) {

        if (restaurantRepo.findByRestaurantname(dto.getRestaurant_name()).isPresent()) {
            throw new RuntimeException("餐厅名已存在，请重新输入餐厅名!");
        }
        else {
            Restaurant newrestaurant = new Restaurant();
            newrestaurant.setLocal(dto.getLocal());
            newrestaurant.setMaxCapacity(dto.getMaxCapacity());
            newrestaurant.setManagerId(dto.getManager_id());
            newrestaurant.setName(dto.getRestaurant_name());
            restaurantRepo.save(newrestaurant);
        }
        return null;
    }

    public List<Restaurant> getAllRestaurants() {
        return restaurantRepo.findAll();
    }

    public List<Restaurant> getRestaurants(Integer id) {
        return restaurantRepo.findowner(id);
    }

    public void deleterestaurant(Integer id, String restaurantname) {

        if (restaurantRepo.findByRestaurantname(restaurantname).isEmpty()) {
            throw new RuntimeException("餐厅不存在!");
        }
        else{
            Restaurant restau =  restaurantRepo.findByRestaurantname(restaurantname).get();
            if (restau.getManagerId() == id) {
                restaurantRepo.delete(restau);
            }
        }


    }
}
