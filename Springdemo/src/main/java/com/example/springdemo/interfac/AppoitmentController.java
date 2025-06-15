package com.example.springdemo.interfac;

import com.example.springdemo.logic.AppointLogit;
import com.example.springdemo.logic.DataRecordService;
import com.example.springdemo.logic.UserLogic;
import com.example.springdemo.pojo.Appointment;
import com.example.springdemo.pojo.ResponseMessage;
import com.example.springdemo.pojo.User;
import com.example.springdemo.pojo.dto.RestaurantDto;
import com.example.springdemo.repo.AppointRepo;
import com.example.springdemo.repo.DataRecordRepo;
import com.example.springdemo.repo.RestaurantRepo;
import com.example.springdemo.repo.UserRepo;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import org.springframework.stereotype.Controller;

import java.util.Objects;

@Controller
@RequestMapping("/user") // URL:localhost:8080/user
public class AppoitmentController {

    @Autowired
    AppointLogit appointLogit;
    @Autowired
    UserLogic userLogic;
    @Autowired
    private AppointRepo appointRepo;

    @GetMapping("/CustomerAppoint")
    public String customerAppointmentPage() {

        return "customerappointment";
    }

    //顾客排队
    @PostMapping("/New_Appoint")
    @ResponseBody
    public ResponseMessage<?> newAppoint(@RequestParam String currentUsername,
                                         @RequestParam String restaurantname) {

        System.out.println(currentUsername);

        User newUser = userLogic.getUserName(currentUsername)
                .orElseThrow(() -> new RuntimeException("用户不存在!"));

        if(!Objects.equals(newUser.getAuthority(), "顾客")){
            throw new SecurityException("Insufficient permissions!");
        }
        Appointment app = appointLogit.makeReservation(currentUsername, restaurantname);
        return ResponseMessage.success(app);
    }

    // 顾客获取自己排队信息
    @GetMapping("/my_Appoint")
    @ResponseBody
    public ResponseMessage<?> my_Appoint(@RequestParam String currentUsername) {

        System.out.println("!"+currentUsername);

        User newUser = userLogic.getUserName(currentUsername)
                .orElseThrow(() -> new RuntimeException("用户不存在!"));

        if(!Objects.equals(newUser.getAuthority(), "顾客")){
            throw new SecurityException("仅顾客可以预约!");
        }
        //Appointment app = appointLogit.getMyReservations(currentUsername);

        Object data = appointLogit.getMyReservations(newUser.getId());
        System.out.println("DEBUG - 返回数据: " + data); // 打印实际数据
        return ResponseMessage.success(data);

        //System.out.println(appointLogit.getMyReservations(newUser.getId()));
        //return ResponseMessage.success(appointLogit.getMyReservations(newUser.getId()));
    }

    // 顾客取消预约
    @DeleteMapping("/cancel_appoint/{id}")
    @ResponseBody
    public ResponseMessage<?> cancel_appoint(@PathVariable("id") int app_id,
                                             @RequestParam String currentUsername) {

        User newUser = userLogic.getUserName(currentUsername)
                .orElseThrow(() -> new RuntimeException("用户不存在!"));

        appointLogit.cancel(app_id, newUser.getId());

        return ResponseMessage.success();

    }

    // 经理获取所有排队信息
    @GetMapping("/manager_Appoint")
    @ResponseBody
    public ResponseMessage<?> manager_Appoint(@RequestParam String currentUsername) {

        System.out.println(currentUsername);

        User newUser = userLogic.getUserName(currentUsername)
                .orElseThrow(() -> new RuntimeException("用户不存在!"));

        if(!Objects.equals(newUser.getAuthority(), "经理")){
            throw new SecurityException("Insufficient permissions!");
        }
        //Appointment app = appointLogit.getMyReservations(currentUsername);
        return ResponseMessage.success(appointLogit.getALLReservations(newUser.getId()));
    }

    //经理处理排队,处理完订单将Waiting改为COMPLETED
    @PostMapping("/appoint_handle")
    @ResponseBody
    public ResponseMessage<?> manager_handle(@RequestParam String currentUsername,
                                              @RequestParam int app_id) {
        System.out.println(currentUsername);

        User newUser = userLogic.getUserName(currentUsername)
                .orElseThrow(() -> new RuntimeException("用户不存在!"));

        if(!Objects.equals(newUser.getAuthority(), "经理")){
            throw new SecurityException("Insufficient permissions!");
        }
        appointLogit.handleappoint(newUser.getId(),app_id);
        return ResponseMessage.success("handle success!");
    }

    // 获取所有排队人数
    @GetMapping("/num_Appoint")
    @ResponseBody
    public ResponseMessage<?> num_Appoint(@RequestParam String currentUsername,
                                          @RequestParam int restaurantId) {

        System.out.println(currentUsername);

        User newUser = userLogic.getUserName(currentUsername)
                .orElseThrow(() -> new RuntimeException("用户不存在!"));

        int uniqueWaitingUsers = appointRepo.countUniqueWaitingUsersByRestaurant(restaurantId);

        return ResponseMessage.success(uniqueWaitingUsers);
    }
}
