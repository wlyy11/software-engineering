package com.example.springdemo.logic;

import com.example.springdemo.pojo.User;
import com.example.springdemo.pojo.Reserve;
import com.example.springdemo.pojo.Retaurant;
import com.example.springdemo.pojo.dto.LoginDto;
import com.example.springdemo.pojo.dto.RegisterDto;
import com.example.springdemo.pojo.dto.UserDto;
import com.example.springdemo.pojo.dto.Reserve;
import com.example.springdemo.repo.UserRepo;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;


import java.util.Collections;
import java.util.Optional;

@Service // spring的bean

public class UserLogic implements IUserLogic {

    
    @Autowired
    private RecordRepo recordRepo;

    @Autowired
    private RestaurantRepo restaurantRepo;

    @Autowired
    private UserRepo userRepo;

    @Autowired
    private ReserveRepo reserveRepo;
    

    @Override
    public User add(UserDto user) {

        User newUser = new User();
        BeanUtils.copyProperties(user,newUser);
        if (userRepo.findByUsername(newUser.getName()).isPresent()) {
            throw new RuntimeException("用户已存在，请重新输入用户名!");
        }
        else {
            return userRepo.save(newUser);   // 增加与修改 自动判别user是否有id，有就是修改，反之增加
        }
    }

    @Override
    public Optional <User> getUserName(String userName) {

        return userRepo.findByUsername(userName);
    }

    @Override
    public User edit(UserDto user) {
        User newUser = new User();
        BeanUtils.copyProperties(user,newUser);
        return userRepo.save(newUser);
    }

    @Override
    public void delete(String userName) {

        if (userRepo.findByUsername(userName).isEmpty()) {
            throw new RuntimeException("用户不存在，请重新输入用户名!");
        }
        else {
            userRepo.deleteById(userRepo.findByUsername(userName).get().getId());
        }
    }

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Override
    public User register(RegisterDto user) {

        if (userRepo.findByUsername(user.getName()).isPresent()) {
            throw new RuntimeException("用户已存在，请重新输入用户名!");
        }
        else{
            user.setPassword(passwordEncoder.encode(user.getPassword()));
            User newUser = new User();
            BeanUtils.copyProperties(user,newUser);
            return userRepo.save(newUser);
        }
    }

    @Override
    public User login(LoginDto user) {

        if (userRepo.findByUsername(user.getName()).isEmpty()) {
            System.out.println(userRepo.findByUsername(user.getName()));
            throw new RuntimeException("用户不存在，请重新输入用户名!");
        }
        else {
            User newuser = userRepo.findByUsername(user.getName()).get();
            if (passwordEncoder.matches(user.getPassword(), newuser.getPassword())){
                return userRepo.findByUsername(user.getName()).get();
            }
            else {
                throw new RuntimeException("密码错误!");
            }
        }
    }

    @Override
        public void changePassword(String username, String oldPassword, String newPassword){

        User user = userRepo.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));

        if (!passwordEncoder.matches(oldPassword, user.getPassword())) {
            throw new RuntimeException("Invalid old password");
        }

        user.setPassword(passwordEncoder.encode(newPassword));
        userRepo.save(user);
    }

    @Override
    public  void deleteUser(String username){

        User user = userRepo.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));
        userRepo.delete(user);
    }

    // ======= 逻辑层功能 =======
    
    //------------顾客预约排队------------
    @Override
    public Reserve makeReservation(String username, int restaurantId, int people, String arrivalEstimate) {
        // 用户验证
        User user = userRepo.findByUsername(username)
                .orElseThrow(() -> new RuntimeException("用户不存在"));
        if (!user.getAuthority().equals("customer")) {
            throw new RuntimeException("仅顾客可以预约");
        }

        // 餐厅验证
        Restaurant restaurant = restaurantRepo.findById(restaurantId)
                .orElseThrow(() -> new RuntimeException("餐厅不存在"));

        // 获取最新记录
        List<Record> records = recordRepo.findByResIdOrderByIdDesc(restaurantId);
        Record latest = records.isEmpty() ? null : records.get(0);

        int current = latest != null ? latest.getPerson() : 0;
        int reserved = latest != null ? latest.getReservedPerson() : 0;

        if (current + reserved + people > restaurant.getMaxCapacity()) {
            throw new RuntimeException("预约失败：小店满员");
        }

        // 创建新的 Record 记录
        Record newRecord = new Record();
        newRecord.setTime(java.time.LocalDateTime.now().toString());
        newRecord.setPerson(current); // 当前人数不变
        newRecord.setReservedPerson(reserved + people); // 预约人数增加
        newRecord.setRes_id(restaurantId);
        recordRepo.save(newRecord);

        // 创建预约记录 Reserve
        Reserve reserve = new Reserve();
        reserve.setUsername(username);
        reserve.setPeople(people);
        reserve.setRestaurantId(restaurantId);
        reserve.setTime(java.time.LocalDateTime.now().toString());
        reserve.setArrivalEstimate(arrivalEstimate); // 设置预计到达时间
        reserveRepo.save(reserve);

        return reserve;
    }

    
    //------------顾客取消预约------------
    @Override
    public void cancelReservation(String username, int reserveId) {
        // 验证用户
        User user = userRepo.findByUsername(username)
                .orElseThrow(() -> new RuntimeException("用户不存在"));
        if (!user.getAuthority().equals("customer")) {
            throw new RuntimeException("仅顾客可以取消预约");
        }

        // 查询预约记录
        Reserve reserve = reserveRepo.findById(reserveId)
                .orElseThrow(() -> new RuntimeException("该预约记录不存在"));

        // 验证预约是否属于该用户
        if (!reserve.getUsername().equals(username)) {
            throw new RuntimeException("您无权取消他人的预约");
        }

        int restaurantId = reserve.getRestaurantId();
        int reservedPeople = reserve.getPeople();

        // 获取餐厅最新一条记录
        List<Record> records = recordRepo.findByResIdOrderByIdDesc(restaurantId);
        if (records.isEmpty()) {
            throw new RuntimeException("餐厅无记录，无法取消预约");
        }

        Record latest = records.get(0);
        if (latest.getReservedPerson() < reservedPeople) {
            throw new RuntimeException("数据异常：已预约人数不足");
        }

        // 新增一条更新后的记录
        Record newRecord = new Record();
        newRecord.setRes_id(restaurantId);
        newRecord.setPerson(latest.getPerson()); // 当前人数不变
        newRecord.setReservedPerson(latest.getReservedPerson() - reservedPeople);
        newRecord.setTime(java.time.LocalDateTime.now().toString());
        recordRepo.save(newRecord);

        // 删除预约记录
        reserveRepo.deleteById(reserveId);
    }
    
    //------------查看餐厅信息------------
    @Override
    public Object getRestaurantInfo(String username, int restaurantId) {
        // 查找用户
        User user = userRepo.findByUsername(username)
                .orElseThrow(() -> new RuntimeException("用户不存在"));
        String authority = user.getAuthority();

        // 查找餐厅
        Restaurant restaurant = restaurantRepo.findById(restaurantId)
                .orElseThrow(() -> new RuntimeException("餐厅不存在"));

        // 查询该餐厅所有记录，按时间升序排列
        List<Record> records = recordRepo.findByResIdOrderByIdAsc(restaurantId);
        if (records.isEmpty()) {
            throw new RuntimeException("该餐厅暂无记录");
        }

        // 经理查看：返回折线图数据（时间、当前人数、预约人数）
        if (authority.equals("manager")) {
            List<String> times = new ArrayList<>();
            List<Integer> currentPersons = new ArrayList<>();
            List<Integer> reservedPersons = new ArrayList<>();

            for (Record r : records) {
                times.add(r.getTime());
                currentPersons.add(r.getPerson());
                reservedPersons.add(r.getReservedPerson());
            }

            // 用 Map 封装返回结构
            Map<String, Object> result = new HashMap<>();
            result.put("restaurantId", restaurant.getId());
            result.put("restaurantName", restaurant.getName());
            result.put("times", times);
            result.put("currentPersons", currentPersons);
            result.put("reservedPersons", reservedPersons);

            return result;

        } else if (authority.equals("customer")) {
            // 顾客只看最新一条记录
            return records.get(records.size() - 1);
        } else {
            throw new RuntimeException("仅顾客和经理可查看餐厅信息");
        }
    }



    
    //------------顾客获取预约信息------------
    @Override
    public List<Reserve> getMyReservations(String username) {
        // 检查用户是否存在
        User user = userRepo.findByUsername(username)
                .orElseThrow(() -> new RuntimeException("用户不存在"));

        // 检查权限是否为顾客
        String authority = user.getAuthority();
        if (!user.getAuthority().equals("customer")) {
            throw new RuntimeException("仅顾客可以查看自己的预约记录");
        }

        // 查询所有该用户的预约记录
        return reserveRepo.findByUsernameOrderByIdDesc(username);
    }

    //------------顾客确认到达餐厅，预约结束------------
    @Override
    public void confirmArrival(String username, int reserveId) {
        // 1. 用户验证
        User user = userRepo.findByUsername(username)
                .orElseThrow(() -> new RuntimeException("用户不存在"));

        if (!user.getAuthority().equals("customer")) {
            throw new RuntimeException("仅顾客可以确认到达");
        }

        // 2. 获取预约信息
        Reserve reserve = reserveRepo.findById(reserveId)
                .orElseThrow(() -> new RuntimeException("预约记录不存在"));

        if (!reserve.getUsername().equals(username)) {
            throw new RuntimeException("您无权确认他人的预约");
        }

        int restaurantId = reserve.getRestaurantId();
        int people = reserve.getPeople();

        // 3. 获取最新记录
        List<Record> records = recordRepo.findByResIdOrderByIdDesc(restaurantId);
        if (records.isEmpty()) {
            throw new RuntimeException("该餐厅无记录，无法确认到达");
        }

        Record latest = records.get(0);

        if (latest.getReservedPerson() < people) {
            throw new RuntimeException("数据异常：预约人数不足");
        }

        // 4. 创建新记录：当前人数增加、预约人数减少
        Record newRecord = new Record();
        newRecord.setRes_id(restaurantId);
        newRecord.setPerson(latest.getPerson() + people);
        newRecord.setReservedPerson(latest.getReservedPerson() - people);

        String now = java.time.LocalDateTime.now()
                .format(java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
        newRecord.setTime(now);

        recordRepo.save(newRecord);

        // 5. 删除该预约记录
        reserveRepo.deleteById(reserveId);
    }



}
