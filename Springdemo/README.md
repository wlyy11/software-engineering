localhost:8080/user/login

启动预测服务
```
cd queue_prediction_service
python -m flask run --host=0.0.0.0 --port=5000
```

启动主服务
```
cd Springdemo
mvn spring-boot:run
```


主要文件`src`构成
```angular2html
\SPRINGDEMO\SRC
│  list.txt
│
├─main
│  ├─java
│  │  └─com
│  │      └─example
│  │          └─springdemo
│  │              │  SpringdemoApplication.java
│  │              │
│  │              ├─exception
│  │              │      GlobalExceptionHandlerAdvice.java
│  │              │      // 异常处理
│  │              ├─interfac  // 控制层与前端相连
│  │              │      AdminApprovalController.java    // 管理员控制层
│  │              │      AppoitmentController.java       // 预约控制层
│  │              │      PythonRunnerService.java        // python执行控制层，执行图像检测人数功能
│  │              │      QueuePredictionController.java  // 预测时间控制层
│  │              │      RecordController.java           // 人数记录控制层
│  │              │      RestaurantController.java       // 餐厅管理控制层
│  │              │      TestController.java             // 预测时间测试层
│  │              │      UserController.java             // 用户管理控制层
│  │              │
│  │              ├─logic
│  │              │      AppointLogit.java               // 预约逻辑层
│  │              │      DataRecordService.java          // 人数记录逻辑层
│  │              │      IRegisterRequestLogic.java      // 管理员逻辑层接口
│  │              │      IUserLogic.java                 // 管理账号逻辑层接口
│  │              │      RegisterRequestLogic.java       // 管理员逻辑层
│  │              │      RestuarantLogit.java            // 餐厅逻辑层
│  │              │      TxtFileReader.java              // txt逻辑层(将图像检测结果写入数据库中)
│  │              │      UserLogic.java                  // 管理账号逻辑层
│  │              │
│  │              ├─pojo
│  │              │  │  Appointment.java                 // 预约类
│  │              │  │  DataRecord.java                  // 人数纪录类
│  │              │  │  QueuePredictionRequest.java      // 预测时间请求类
│  │              │  │  QueuePredictionResponse.java     // 预测时间类
│  │              │  │  ResponseMessage.java             // 后端返回信息类
│  │              │  │  Restaurant.java                  // 餐厅类
│  │              │  │  User.java                        // 用户类
│  │              │  │  User_Audit.java                  // 用户审批类
│  │              │  │
│  │              │  └─dto
│  │              │          ChangePasswordRequest.java  // 修改密码请求类
│  │              │          DeleteUserRequest.java      // 删除用户请求类
│  │              │          LoginDto.java               // 登录用户请求类
│  │              │          RegisterDto.java            // 注册用户请求类
│  │              │          RestaurantDto.java          // 餐厅请求类
│  │              │          UserDto.java                // 用户请求类
│  │              │
│  │              ├─repo
│  │              │      AppointRepo.java                // 预约数据层
│  │              │      AuditRepo.java                  // 用户审批数据层
│  │              │      DataRecordRepo.java             // 人数记录数据层
│  │              │      RegisterRequestRepo.java        // 用户注册数据层
│  │              │      RestaurantRepo.java             // 餐厅数据层
│  │              │      UserRepo.java                   // 用户数据层
│  │              │
│  │              └─security   // 可以忽略
│  │                      CorsConfig.java
│  │                      CustomUserDetailsService.java
│  │                      JwtAuthFilter.java
│  │                      JwtUtil.java
│  │                      Key.java
│  │                      SecurityConfig.java
│  │
│  └─resources
│      │  application.properties
│      │
│      └─templates   // 前端文件
│          │  change-password.html
│          │  customer.html
│          │  customerappointment.html
│          │  login.html
│          │  register.html
│          │  Restaurant.html
│          │  user.html
│
└─test
└─java
└─com
└─example
└─springdemo
SpringdemoApplicationTests.java


```

测试流程：使用API fox

注意：注册用户等不需要JWT的Token

1. 首先运行`SpringdemoApplication.java`启动项目，获得使用的端口(我的是8080)；
2. 打开API fox，按照对应URL进行对应的操作，例如：注册账号，`Post localhost:8080/user/register`,再在Body中输入注册的账号名密码和权限，如图![image/img.png](image/img.png)账号注册后返回消息，正确创建后会返回用户id，name，密码(已加密)，以及权限![img_1.png](image/img_1.png)
3. 登录账号`Psot localhost:8080/user/login`，Body输入登录用户名和密码(注意是username不是name)![image/img_2.png](image/img_2.png)成功登录后会返回Token ![image/img_3.png](image/img_3.png)
4. 接着在API fox 中手动添加 Authorization 头，切换到 "Headers" 选项卡，点击 "添加参数"

    在 Key 列输入：`Authorization`

    在 Value 列输入：`Bearer <您的JWT令牌>`,例如 `Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ3bHl5eSIsImlhdCI6MTc0ODg2NDIwMiwiZXhwIjoxODM1MjY0MjAyfQ.5PYRqNa_ep8znJtraV8mVJGKXGffsdWzBuPDu_IzchpgrTax6ZJZ-BdW0eyH5BocUNzt0BTRaSyGM8xEGloa8Q` 
5. 最后修改密码，![image/img_4.png](image/img_4.png) 修改其他账号的密码无法成功并抛出错误`You can only change your own password` ![image/img_5.png](image/img_5.png)

管理员审批权限，测试流程
首先登录sa账号，添加Token
Get localhost:8080/user/admin/approvals/pending  获得待处理的请求

处理请求，也需添加Token。  添加 Path参数 requestId，添加Query 参数 approved
localhost:8080/user/admin/approvals/{requestId}/handle?approved=false



