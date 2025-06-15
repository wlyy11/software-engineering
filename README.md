
### 1. 启动预测服务
```bash
cd queue_prediction_service
python -m flask run --host=0.0.0.0 --port=5000
```

### 2. 启动主服务
```bash
cd Springdemo
mvn spring-boot:run
```

新增新建餐厅，查看餐厅，参看餐厅人数以及排队预约功能，后端功能还差预测时间和生成人数曲线图图像

API测试：

经理新建餐厅：localhost:8080/user/New_Restaurant
需要在Params中添加参数currentUsername，
后端`@RequestParam String currentUsername`基本都需要。只有经理才能查看餐厅

顾客查看所有的餐厅：localhost:8080/user/viewRestaurant?currentUsername=wlyy
需要在Params中添加参数currentUsername

经理查看自己管理的餐厅:localhost:8080/user/viewOwnerRestaurant
需要在Params中添加参数currentUsername

查看最新的餐厅人数，顾客：localhost:8080/user/record
需要在Params中添加参数currentUsername和res_name(餐厅名字)

经理查看最近10条记录：localhost:8080/user/record_viewManager
需要在Params中添加参数currentUsername和res_name(餐厅名字)

经理查看某个日期的人数记录：localhost:8080/user/record_viewDate
需要在Params中添加参数currentUsername和res_name(餐厅名字)，date(日期：严格按照格式6_09_12_05)

顾客预约排队：localhost:8080/user/New_Appoint
需要在Params中添加参数currentUsername和res_name(餐厅名字)

顾客查看自己排队记录：localhost:8080/user/my_Appoint
需要在Params中添加参数currentUsername

经理查看自己管理餐厅的所有排队记录：localhost:8080/user/manager_Appoint
需要在Params中添加参数currentUsername

经理处理排队记录，将Waiting改为COMPLETED：localhost:8080/user/appoint_handle
需要在Params中添加参数currentUsername和预约号app_id

修改异常类，可以返回具体的错误类型

基于Spring Boot 实现了用户账号注册，登录，修改密码以及注销账号的功能

主要文件`src`构成
```angular2html
│  README.md
│  
├─main
│  ├─java
│  │  └─com
│  │      └─example
│  │          └─springdemo
│  │              │  SpringdemoApplication.java  //主程序，项目入口
│  │              ├─exception
│  │              │      GlobalExceptionHandlerAdvice.java //异常类
│  │              ├─interfac
│  │              │      UserController.java     //界面层
│  │              │      AdminApprovalController //管理员界面层
│  │              │      PythonRunnerService     //python运行层
│  │              │      RecordController        //人数记录界面层
│  │              │      RestaurantController    //餐厅界面层
│  │              ├─logic
│  │              │      IUserLogic.java         //逻辑层接口
│  │              │      UserLogic.java          //逻辑层
│  │              │      IRegisterRequestLogic   //管理员逻辑层接口
│  │              │      RegisterRequestLogic    //管理员逻辑层
│  │              │      AppointLogit.java       //预约逻辑层
│  │              │      DataRecordService.java  //人数记录逻辑层
│  │              │      RestuarantLogit.java    //餐厅逻辑层
│  │              │      TxtFileReader.java      //文档读写逻辑层
│  │              ├─model                        //模型层
│  │              ├─pojo                         //各种类的实现
│  │              │  │  Record.java              //记录人数类
│  │              │  │  ResponseMessage.java     //返回信息类
│  │              │  │  Restaurant.java          //餐厅类
│  │              │  │  User.java                //用户类
│  │              │  │  User_Audit               //用户账号请求类
│  │              │  │  Appointment              //预约类
│  │              │  └─dto                       //操作类
│  │              │          ChangePasswordRequest.java //修改密码类
│  │              │          DeleteUserRequest.java     //注销账号类
│  │              │          LoginDto.java              //登录类
│  │              │          RegisterDto.java           //注册账号类
│  │              │          UserDto.java               //用户操作类
│  │              │          RestaurantDto.java         //餐厅注册类
│  │              ├─repo
│  │              │      UserRepo.java           
                  |      //数据层(用于对数据库进行增删改查操作)
│  │              │      RegisterRequestRepo
                  |      //账号请求数据层
│  │              │      AppointRepo
                  |      //预约数据层
│  │              │      RestaurantRepo
                  |      //餐厅数据层
│  │              │      DataRecordRepo
                  |      //人数记录数据层
│  │              └─security  
                    //安全类(使用JWT，当用户登录后生成一个Token密钥，
                    //      用户使用这个Token才能修改密码注销账号，
                    //      保证了用户只能操作自己的账号)
│  │                      CustomUserDetailsService.java //用户细节类
│  │                      JwtAuthFilter.java            //JWT过滤类
│  │                      JwtUtil.java                  //JWT类
│  │                      Key.java                      //生成密钥类
│  │                      SecurityConfig.java           //安全配置类
│  └─resources
│      │  application.properties   各种参数的配置
│      ├─static
│      └─templates
└─test     测试，暂时没有实现
```

测试流程：使用API fox

1. 首先运行`SpringdemoApplication.java`启动项目，获得使用的端口(我的是8080)；
2. 打开API fox，按照对应URL进行对应的操作，例如：注册账号，`Post localhost:8080/user/register`,再在Body中输入注册的账号名密码和权限，如图![img.png](image/img.png)账号注册后返回消息，正确创建后会返回用户id，name，密码(已加密)，以及权限![img_1.png](image/img_1.png)
3. 登录账号`Psot localhost:8080/user/login`，Body输入登录用户名和密码(注意是username不是name)![img_2.png](image/img_2.png)成功登录后会返回Token ![img_3.png](image/img_3.png)
4. 接着在API fox 中手动添加 Authorization 头，切换到 "Headers" 选项卡，点击 "添加参数"

    在 Key 列输入：`Authorization`

    在 Value 列输入：`Bearer <您的JWT令牌>`,例如 `Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ3bHl5eSIsImlhdCI6MTc0ODg2NDIwMiwiZXhwIjoxODM1MjY0MjAyfQ.5PYRqNa_ep8znJtraV8mVJGKXGffsdWzBuPDu_IzchpgrTax6ZJZ-BdW0eyH5BocUNzt0BTRaSyGM8xEGloa8Q` 
5. 最后修改密码，![img_4.png](image/img_4.png) 修改其他账号的密码无法成功并抛出错误`You can only change your own password` ![img_5.png](image/img_5.png)

管理员审批权限，测试流程
首先登录sa账号，添加Token
Get localhost:8080/user/admin/approvals/pending  获得待处理的请求

处理请求，也需添加Token。  添加 Path参数 requestId，添加Query 参数 approved
localhost:8080/user/admin/approvals/{requestId}/handle?approved=false



