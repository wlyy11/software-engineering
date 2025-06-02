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
│  │              ├─logic
│  │              │      IUserLogic.java         //逻辑层接口
│  │              │      UserLogic.java          //逻辑层
│  │              ├─model                        //模型层
│  │              ├─pojo                         //各种类的实现
│  │              │  │  Record.java              //记录人数类
│  │              │  │  ResponseMessage.java     //返回信息类
│  │              │  │  Restaurant.java          //餐厅类
│  │              │  │  User.java                //用户类
│  │              │  └─dto                       //操作类
│  │              │          ChangePasswordRequest.java //修改密码类
│  │              │          DeleteUserRequest.java     //注销账号类
│  │              │          LoginDto.java              //登录类
│  │              │          RegisterDto.java           //注册账号类
│  │              │          UserDto.java               //用户操作类
│  │              ├─repo
│  │              │      UserRepo.java           
                  |      //数据层(用于对数据库进行增删改查操作)
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


需要改进：目前不清楚前端登录后怎么自动保存Token，手动添加很麻烦，请之后负责前端以及界面层的同学修改