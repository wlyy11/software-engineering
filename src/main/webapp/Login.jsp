<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>餐厅人流量监测系统 - 登录注册</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 0; 
            background-color: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .header { 
            position: absolute;
            top: 0;
            width: 100%;
            background-color: #2c3e50; 
            color: white; 
            padding: 15px 20px; 
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .container {
            width: 100%;
            max-width: 400px;
            margin-top: 80px;
        }
        .card { 
            background: white; 
            border-radius: 5px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
            padding: 30px;
        }
        .card-title { 
            font-size: 20px; 
            font-weight: bold; 
            margin-bottom: 20px; 
            color: #2c3e50;
            text-align: center;
        }
        .form-group { 
            margin-bottom: 20px; 
        }
        .form-group label { 
            display: block; 
            margin-bottom: 8px; 
            font-weight: bold;
            color: #2c3e50;
        }
        input[type="text"], 
        input[type="password"], 
        input[type="email"],
        select { 
            padding: 12px; 
            width: 100%; 
            border: 1px solid #ddd; 
            border-radius: 4px;
            box-sizing: border-box;
            font-size: 16px;
        }
        .btn { 
            padding: 12px; 
            width: 100%;
            color: white; 
            border: none; 
            border-radius: 4px; 
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
        }
        .btn-primary { 
            background-color: #3498db; 
        }
        .btn-success { 
            background-color: #2ecc71; 
        }
        .btn-secondary {
            background-color: #95a5a6;
        }
        .tab-container { 
            margin-bottom: 20px; 
        }
        .tab-buttons { 
            display: flex; 
            border-bottom: 2px solid #ddd; 
        }
        .tab-button { 
            padding: 12px 20px; 
            background: none; 
            border: none; 
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            color: #7f8c8d;
            flex: 1;
            text-align: center;
        }
        .tab-button.active { 
            color: #2c3e50;
            border-bottom: 3px solid #3498db; 
        }
        .tab-content { 
            display: none; 
            padding: 20px 0 0;
        }
        .tab-content.active { 
            display: block; 
        }
        .switch-text {
            text-align: center;
            margin-top: 20px;
            color: #7f8c8d;
        }
        .switch-link {
            color: #3498db;
            cursor: pointer;
            font-weight: bold;
        }
        .error-message {
            color: #e74c3c;
            text-align: center;
            margin-bottom: 15px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>欢迎使用餐厅人流量监测系统</h1>
    </div>
    
    <div class="container">
        <div class="card">
            <div class="tab-container">
                <div class="tab-buttons">
                    <button class="tab-button active" onclick="switchTab('login')">登录</button>
                    <button class="tab-button" onclick="switchTab('register')">注册</button>
                </div>
                
                <!-- 登录表单 -->
                <div id="login" class="tab-content active">
                    <div class="card-title">用户登录</div>
                    
                    <%-- 错误消息显示 --%>
                    <% if (request.getAttribute("loginError") != null) { %>
                        <div class="error-message"><%= request.getAttribute("loginError") %></div>
                    <% } %>
                    
                    <form action="LoginServlet" method="post">
                        <input type="hidden" name="action" value="login">
                        
                        <div class="form-group">
                            <label for="login_username">用户名</label>
                            <input type="text" id="login_username" name="username" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="login_password">密码</label>
                            <input type="password" id="login_password" name="password" required>
                        </div>
                        
                        <button type="submit" class="btn btn-primary">登录</button>
                    </form>
                    
                    <div class="switch-text">
                        还没有账号？<span class="switch-link" onclick="switchTab('register')">立即注册</span>
                    </div>
                </div>
                
                <!-- 注册表单 -->
                <div id="register" class="tab-content">
                    <div class="card-title">用户注册</div>
                    
                    <%-- 错误消息显示 --%>
                    <% if (request.getAttribute("registerError") != null) { %>
                        <div class="error-message"><%= request.getAttribute("registerError") %></div>
                    <% } %>
                    
                    <%-- 成功消息显示 --%>
                    <% if (request.getAttribute("registerSuccess") != null) { %>
                        <div class="error-message" style="color: #2ecc71;"><%= request.getAttribute("registerSuccess") %></div>
                    <% } %>
                    
                    <form action="LoginServlet" method="post">
                        <input type="hidden" name="action" value="register">
                        
                        <div class="form-group">
                            <label for="reg_username">用户名</label>
                            <input type="text" id="reg_username" name="username" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="reg_password">密码</label>
                            <input type="password" id="reg_password" name="password" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="reg_confirm_password">确认密码</label>
                            <input type="password" id="reg_confirm_password" name="confirm_password" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="reg_email">电子邮箱</label>
                            <input type="email" id="reg_email" name="email" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="reg_phone">手机号码</label>
                            <input type="text" id="reg_phone" name="phone" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="reg_role">注册身份</label>
                            <select id="reg_role" name="role" required>
                                <option value="">-- 请选择身份 --</option>
                                <option value="customer">顾客</option>
                                <option value="manager">经理</option>
                            </select>
                            <small style="color: #7f8c8d; display: block; margin-top: 5px;">注：管理员账号需联系系统管理员创建</small>
                        </div>
                        
                        <button type="submit" class="btn btn-success">注册</button>
                    </form>
                    
                    <div class="switch-text">
                        已有账号？<span class="switch-link" onclick="switchTab('login')">立即登录</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // 切换登录/注册标签页
        function switchTab(tabId) {
            // 更新活动标签按钮样式
            document.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.remove('active');
            });
            document.querySelector(`.tab-button[onclick="switchTab('${tabId}')"]`).classList.add('active');
            
            // 显示对应的内容
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(tabId).classList.add('active');
        }
        
        // 处理URL参数，如从注册成功跳转回登录页
        document.addEventListener('DOMContentLoaded', function() {
            const urlParams = new URLSearchParams(window.location.search);
            const showTab = urlParams.get('show');
            
            if (showTab === 'login') {
                switchTab('login');
            } else if (showTab === 'register') {
                switchTab('register');
            }
        });
        
        // 密码确认验证
        document.getElementById('reg_password').addEventListener('input', validatePassword);
        document.getElementById('reg_confirm_password').addEventListener('input', validatePassword);
        
        function validatePassword() {
            const password = document.getElementById('reg_password').value;
            const confirmPassword = document.getElementById('reg_confirm_password').value;
            const submitBtn = document.querySelector('#register form button[type="submit"]');
            
            if (confirmPassword && password !== confirmPassword) {
                document.getElementById('reg_confirm_password').style.borderColor = '#e74c3c';
                submitBtn.disabled = true;
                submitBtn.style.opacity = '0.6';
                submitBtn.style.cursor = 'not-allowed';
            } else {
                document.getElementById('reg_confirm_password').style.borderColor = '#ddd';
                submitBtn.disabled = false;
                submitBtn.style.opacity = '1';
                submitBtn.style.cursor = 'pointer';
            }
        }
    </script>
</body>
</html>