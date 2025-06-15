package com.example.springdemo.logic;

import com.example.springdemo.pojo.Appointment;
import com.example.springdemo.pojo.DataRecord;
import com.example.springdemo.pojo.Restaurant;
import com.example.springdemo.pojo.User;
import com.example.springdemo.repo.AppointRepo;
import com.example.springdemo.repo.DataRecordRepo;
import com.example.springdemo.repo.RestaurantRepo;
import com.example.springdemo.repo.UserRepo;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service // spring的bean
public class AppointLogit {
    @Autowired
    private DataRecordRepo recordRepo;

    @Autowired
    private RestaurantRepo restaurantRepo;

    @Autowired
    private UserRepo userRepo;

    @Autowired
    private AppointRepo appointRepo;


    public Appointment makeReservation(String username, String res_name) {
        // 用户验证
        User user = userRepo.findByUsername(username)
                .orElseThrow(() -> new RuntimeException("用户不存在"));
        if (!user.getAuthority().equals("顾客")) {
            throw new RuntimeException("仅顾客可以预约");
        }

        // 餐厅验证
        Restaurant restaurant = restaurantRepo.findByRestaurantname(res_name)
                .orElseThrow(() -> new RuntimeException("餐厅不存在"));

        // 获取最新记录
        int res_id = restaurant.getId();System.out.println(res_id);
        DataRecord now_record =  recordRepo.findLatestRecord(res_id)
                .orElseThrow(() -> new RuntimeException("无记录"));

        int current = now_record.getPerson();
        int appoint_num = appointRepo.findnumAppoint();

        System.out.println(appoint_num);System.out.println(current);

        if (current +  appoint_num > restaurant.getMaxCapacity()) {
            throw new RuntimeException("预约失败：小店满员");
        }

        Appointment appoint = new Appointment();
        appoint.setRestaurant(restaurant);
        appoint.setUser(user);
        appoint.setStatus(Appointment.AppointStatus.WAITING);
        appointRepo.save(appoint);
        return appoint;
    }

    //获得自己的预约信息
    public List<Appointment> getMyReservations(int id) {

        return appointRepo.findUserAppoint(id);
    }

    //经理获得所有的预约信息
    public List<Appointment> getALLReservations(int id) {


        return appointRepo.findALLAppoint(id);
    }

    //处理appoint
    public void handleappoint(int user_id, int app_id) {

        Appointment app = appointRepo.findById(app_id)
                .orElseThrow(() -> new EntityNotFoundException("预约不存在"));

        Restaurant restau = app.getRestaurant();
        if(restau.getManagerId()!=user_id) {
            throw new RuntimeException("不能处理其他餐厅的排队信息!");
        }

        app.setStatus(Appointment.AppointStatus.COMPLETED);
        appointRepo.save(app);

    }

    public void cancel(int app_id, int user_id) {

        if (appointRepo.findById(app_id).isEmpty()) {
            throw new RuntimeException("记录不存在!");
        }
        else {
            if (appointRepo.findById(app_id).get().getUser().getId() != user_id) {
                throw new RuntimeException("无法取消其他用户的预约!");
            }
            appointRepo.deleteById(appointRepo.findById(app_id).get().getId());
        }
    }
}
