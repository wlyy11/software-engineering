<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.sql.*" %>
<%!
    // 数据库连接方法
    public Connection getConnection() throws SQLException {
        String url = "jdbc:mysql://localhost:3306/restaurant_customer_db";
        String username = "customer";
        String password = "customer123";
        try {
            Class.forName("com.mysql.jdbc.Driver");
            return DriverManager.getConnection(url, username, password);
        } catch (ClassNotFoundException e) {
            throw new SQLException("JDBC Driver not found", e);
        }
    }
%>
<html>
<head>
    <title>餐厅人流量监测系统 - 顾客界面</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }
        .header { 
            background-color: #2c3e50; 
            color: white; 
            padding: 15px 20px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .main-container { 
            display: flex; 
            min-height: calc(100vh - 60px);
        }
        .sidebar { 
            width: 220px; 
            background-color: #34495e; 
            color: white; 
            padding: 20px 0;
        }
        .sidebar a { 
            display: block; 
            color: #ecf0f1; 
            padding: 12px 20px; 
            text-decoration: none;
            transition: background 0.3s;
        }
        .sidebar a:hover, .sidebar a.active { 
            background-color: #2c3e50; 
        }
        .content { 
            flex: 1; 
            padding: 20px; 
            background-color: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
        }
        .card { 
            background: white; 
            border-radius: 5px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
            margin-bottom: 20px; 
            padding: 20px;
        }
        .card-title { 
            font-size: 18px; 
            font-weight: bold; 
            margin-bottom: 15px; 
            color: #2c3e50;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }
        .btn { 
            padding: 8px 15px; 
            background-color: #3498db; 
            color: white; 
            border: none; 
            border-radius: 4px; 
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
        }
        .btn-primary { background-color: #3498db; }
        .btn-success { background-color: #2ecc71; }
        .btn-warning { background-color: #f39c12; }
        .btn-danger { background-color: #e74c3c; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="text"], input[type="number"], input[type="datetime-local"], input[type="tel"], select { 
            padding: 10px; 
            width: 100%; 
            border: 1px solid #ddd; 
            border-radius: 4px;
            box-sizing: border-box;
        }
        .restaurant-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .restaurant-card {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        .restaurant-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .restaurant-name {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
        }
        .restaurant-location {
            color: #7f8c8d;
            margin-bottom: 15px;
        }
        .crowd-indicator {
            height: 20px;
            background-color: #f1f1f1;
            border-radius: 10px;
            margin-bottom: 15px;
            overflow: hidden;
        }
        .crowd-level {
            height: 100%;
            background-color: #2ecc71;
            width: 30%; /* 根据实际拥挤程度调整 */
        }
        .crowd-status {
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
        }
        .crowd-label {
            font-size: 14px;
            color: #7f8c8d;
        }
        .crowd-value {
            font-weight: bold;
            color: #2c3e50;
        }
        .traffic-image {
            width: 100%;
            height: 180px;
            background-color: #f1f1f1;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }
        .traffic-image img {
            max-width: 100%;
            max-height: 100%;
            object-fit: cover;
        }
        .queue-number {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #e74c3c;
            margin: 20px 0;
            display: none;
        }
        .reminder-set {
            text-align: center;
            color: #2ecc71;
            font-weight: bold;
            margin: 20px 0;
            display: none;
        }
        .loading {
            display: none;
            margin: 20px 0;
            text-align: center;
            color: #7f8c8d;
        }
        .tab-container { margin-bottom: 20px; }
        .tab-buttons { display: flex; border-bottom: 1px solid #ddd; }
        .tab-button { 
            padding: 10px 20px; 
            background: none; 
            border: none; 
            cursor: pointer;
            border-bottom: 3px solid transparent;
        }
        .tab-button.active { 
            border-bottom: 3px solid #3498db; 
            font-weight: bold;
        }
        .tab-content { display: none; padding: 15px 0; }
        .tab-content.active { display: block; }
    </style>
</head>
<body>
    <div class="header">
        <h2>餐厅人流量监测系统 - 顾客界面</h2>
        <div>
            <span style="margin-right: 15px;">
                <% if (session.getAttribute("customer_name") != null) { %>
                    欢迎, <%= session.getAttribute("customer_name") %>
                <% } else { %>
                    您好，顾客
                <% } %>
            </span>
            <% if (session.getAttribute("customer_name") != null) { %>
                <a href="logout.jsp" style="color: white; text-decoration: none;">退出</a>
            <% } else { %>
                <a href="login.jsp" style="color: white; text-decoration: none;">登录</a>
            <% } %>
        </div>
    </div>
    
    <div class="main-container">
        <div class="sidebar">
            <a href="#traffic" class="active">人流量查看</a>
            <a href="#reservation">预约排队</a>
            <a href="#myqueue">我的排队</a>
            <a href="#profile">个人资料</a>
        </div>
        
        <div class="content">
            <!-- 人流量查看 -->
            <div id="traffic" class="card">
                <div class="card-title">餐厅人流量实时查看</div>
                
                <form method="get" action="#traffic">
                    <div style="display: flex; gap: 15px;">
                        <div class="form-group" style="flex: 2;">
                            <label for="search_restaurant">搜索餐厅</label>
                            <input type="text" id="search_restaurant" name="search_restaurant" 
                                   placeholder="输入餐厅名称或位置" 
                                   value="<%= request.getParameter("search_restaurant") != null ? request.getParameter("search_restaurant") : "" %>">
                        </div>
                        <div class="form-group" style="flex: 1;">
                            <label for="crowd_level">拥挤程度</label>
                            <select id="crowd_level" name="crowd_level">
                                <option value="">全部</option>
                                <option value="low" <%= "low".equals(request.getParameter("crowd_level")) ? "selected" : "" %>>空闲</option>
                                <option value="medium" <%= "medium".equals(request.getParameter("crowd_level")) ? "selected" : "" %>>适中</option>
                                <option value="high" <%= "high".equals(request.getParameter("crowd_level")) ? "selected" : "" %>>拥挤</option>
                            </select>
                        </div>
                        <div style="align-self: flex-end;">
                            <button type="submit" class="btn btn-primary">搜索</button>
                        </div>
                    </div>
                </form>
                
                <div class="restaurant-grid">
                    <%
                        String searchRestaurant = request.getParameter("search_restaurant");
                        String crowdLevel = request.getParameter("crowd_level");
                        
                        String query = "SELECT r.id, r.name, r.location, r.image_path, " +
                                      "rs.current_count, rs.max_capacity, rs.crowd_level, rs.last_update " +
                                      "FROM restaurants r " +
                                      "JOIN realtime_stats rs ON r.id = rs.restaurant_id " +
                                      "WHERE 1=1";
                        
                        if (searchRestaurant != null && !searchRestaurant.isEmpty()) {
                            query += " AND (r.name LIKE '%" + searchRestaurant + "%' OR r.location LIKE '%" + searchRestaurant + "%')";
                        }
                        if (crowdLevel != null && !crowdLevel.isEmpty()) {
                            query += " AND rs.crowd_level = '" + crowdLevel + "'";
                        }
                        query += " ORDER BY rs.last_update DESC";
                        
                        try (Connection conn = getConnection();
                             Statement stmt = conn.createStatement();
                             ResultSet rs = stmt.executeQuery(query)) {
                            while (rs.next()) {
                                int currentCount = rs.getInt("current_count");
                                int maxCapacity = rs.getInt("max_capacity");
                                int percentage = (int) Math.round((double) currentCount / maxCapacity * 100);
                                String crowdColor = "#2ecc71"; // 绿色
                                if (percentage > 70) crowdColor = "#e74c3c"; // 红色
                                else if (percentage > 40) crowdColor = "#f39c12"; // 黄色
                    %>
                    <div class="restaurant-card">
                        <div class="restaurant-name"><%= rs.getString("name") %></div>
                        <div class="restaurant-location"><%= rs.getString("location") %></div>
                        
                        <div class="crowd-status">
                            <div>
                                <div class="crowd-label">当前人数</div>
                                <div class="crowd-value"><%= currentCount %>/<%= maxCapacity %></div>
                            </div>
                            <div>
                                <div class="crowd-label">拥挤程度</div>
                                <div class="crowd-value"><%= rs.getString("crowd_level") %></div>
                            </div>
                            <div>
                                <div class="crowd-label">更新时间</div>
                                <div class="crowd-value">
                                    <%= rs.getTimestamp("last_update").toString().substring(11, 16) %>
                                </div>
                            </div>
                        </div>
                        
                        <div class="crowd-indicator">
                            <div class="crowd-level" style="width: <%= percentage %>%; background-color: <%= crowdColor %>;"></div>
                        </div>
                        
                        <div class="traffic-image">
                            <%
                                String imagePath = rs.getString("image_path");
                                if (imagePath != null && !imagePath.isEmpty()) {
                            %>
                            <img src="<%= imagePath %>" alt="<%= rs.getString("name") %>实时画面">
                            <%
                                } else {
                            %>
                            <p>暂无实时画面</p>
                            <%
                                }
                            %>
                        </div>
                        
                        <div style="display: flex; gap: 10px;">
                            <a href="#reservation?restaurant_id=<%= rs.getInt("id") %>" class="btn btn-primary">预约排队</a>
                            <a href="restaurant_detail.jsp?id=<%= rs.getInt("id") %>" class="btn">查看详情</a>
                        </div>
                    </div>
                    <%
                            }
                        } catch (SQLException e) {
                            out.println("<p>数据库错误: " + e.getMessage() + "</p>");
                        }
                    %>
                </div>
            </div>
            
            <!-- 预约排队 -->
            <div id="reservation" class="card" style="display: none;">
                <div class="card-title">餐厅预约排队</div>
                
                <form id="queueForm" method="post">
                    <div class="form-group">
                        <label for="queue_restaurant">选择餐厅</label>
                        <select id="queue_restaurant" name="restaurant_id" required>
                            <option value="">-- 请选择餐厅 --</option>
                            <%
                                String restaurantQuery = "SELECT r.id, r.name, rs.current_count, rs.estimated_wait_time " +
                                                       "FROM restaurants r " +
                                                       "JOIN realtime_stats rs ON r.id = rs.restaurant_id " +
                                                       "ORDER BY r.name";
                                
                                try (Connection conn = getConnection();
                                     Statement stmt = conn.createStatement();
                                     ResultSet rs = stmt.executeQuery(restaurantQuery)) {
                                    
                                    String selectedRestaurantId = request.getParameter("restaurant_id");
                                    
                                    while (rs.next()) {
                                        String waitTime = rs.getInt("estimated_wait_time") + "分钟";
                                        String crowdInfo = rs.getInt("current_count") + "人在店";
                            %>
                            <option value="<%= rs.getString("id") %>" <%= selectedRestaurantId != null && selectedRestaurantId.equals(rs.getString("id")) ? "selected" : "" %>>
                                <%= rs.getString("name") %> (<%= crowdInfo %>, 预计等待<%= waitTime %>)
                            </option>
                            <%
                                    }
                                } catch (SQLException e) {
                                    out.println("<p>数据库错误: " + e.getMessage() + "</p>");
                                }
                            %>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="queue_party_size">用餐人数</label>
                        <select id="queue_party_size" name="party_size" required>
                            <option value="1">1人</option>
                            <option value="2">2人</option>
                            <option value="3">3人</option>
                            <option value="4">4人</option>
                            <option value="5">5人</option>
                            <option value="6">6人</option>
                            <option value="7">7-10人</option>
                            <option value="10">10人以上</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="customer_name">姓名</label>
                        <input type="text" id="customer_name" name="customer_name" 
                               value="<%= session.getAttribute("customer_name") != null ? session.getAttribute("customer_name") : "" %>" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="customer_phone">手机号码</label>
                        <input type="tel" id="customer_phone" name="customer_phone" 
                               value="<%= session.getAttribute("customer_phone") != null ? session.getAttribute("customer_phone") : "" %>" required>
                    </div>
                    
                    <div id="estimatedWaitTime" style="margin: 15px 0; padding: 10px; background-color: #f8f9fa; border-radius: 5px; display: none;">
                        <strong>预计等待时间:</strong> <span id="waitTimeValue">30分钟</span>
                    </div>
                    
                    <button type="button" onclick="joinQueue()" class="btn btn-success">加入排队</button>
                </form>
                
                <div id="queueLoading" class="loading">
                    <p>正在处理您的排队请求，请稍候...</p>
                </div>
                
                <div id="queueResult" class="queue-number" style="display: none;">
                    您的排队号码: <span id="queueNumber">A102</span>
                </div>
                
                <div id="reminderSection" style="margin-top: 20px; display: none;">
                    <h3>设置排队提醒</h3>
                    <form id="reminderForm">
                        <div class="form-group">
                            <label for="reminder_time">提前提醒时间</label>
                            <select id="reminder_time" name="reminder_time">
                                <option value="5">提前5分钟</option>
                                <option value="10" selected>提前10分钟</option>
                                <option value="15">提前15分钟</option>
                                <option value="20">提前20分钟</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="reminder_method">提醒方式</label>
                            <select id="reminder_method" name="reminder_method">
                                <option value="sms">短信提醒</option>
                                <option value="app">APP通知</option>
                                <option value="both">短信+APP</option>
                            </select>
                        </div>
                        
                        <button type="button" onclick="setReminder()" class="btn btn-primary">设置提醒</button>
                    </form>
                    
                    <div id="reminderSet" class="reminder-set" style="display: none;">
                        提醒设置成功！您将在排队快到号时收到通知。
                    </div>
                </div>
            </div>
            
            <!-- 我的排队 -->
            <div id="myqueue" class="card" style="display: none;">
                <div class="card-title">我的当前排队</div>
                
                <%
                    if (session.getAttribute("customer_id") == null) {
                %>
                <div style="text-align: center; padding: 40px;">
                    <p>您尚未登录，无法查看排队信息</p>
                    <a href="login.jsp" class="btn btn-primary">立即登录</a>
                </div>
                <%
                    } else {
                        try (Connection conn = getConnection();
                             PreparedStatement pstmt = conn.prepareStatement(
                                 "SELECT q.id, q.queue_number, q.join_time, q.estimated_wait_time, q.status, " +
                                 "r.name AS restaurant_name, r.location " +
                                 "FROM queue q " +
                                 "JOIN restaurants r ON q.restaurant_id = r.id " +
                                 "WHERE q.customer_id = ? AND q.status IN ('waiting', 'notified') " +
                                 "ORDER BY q.join_time DESC")) {
                            
                            pstmt.setInt(1, (Integer) session.getAttribute("customer_id"));
                            ResultSet rs = pstmt.executeQuery();
                            
                            if (!rs.isBeforeFirst()) {
                %>
                <div style="text-align: center; padding: 40px;">
                    <p>您当前没有正在进行的排队</p>
                    <a href="#reservation" class="btn btn-primary">立即预约排队</a>
                </div>
                <%
                            } else {
                                while (rs.next()) {
                                    String statusText = "";
                                    String statusClass = "";
                                    if ("waiting".equals(rs.getString("status"))) {
                                        statusText = "排队中";
                                        statusClass = "btn-primary";
                                    } else if ("notified".equals(rs.getString("status"))) {
                                        statusText = "即将到号";
                                        statusClass = "btn-warning";
                                    }
                %>
                <div class="restaurant-card" style="margin-bottom: 15px;">
                    <div class="restaurant-name"><%= rs.getString("restaurant_name") %></div>
                    <div class="restaurant-location"><%= rs.getString("location") %></div>
                    
                    <div style="display: flex; justify-content: space-between; margin: 15px 0;">
                        <div>
                            <div style="font-size: 14px; color: #7f8c8d;">排队号码</div>
                            <div style="font-size: 24px; font-weight: bold; color: #e74c3c;"><%= rs.getString("queue_number") %></div>
                        </div>
                        <div>
                            <div style="font-size: 14px; color: #7f8c8d;">预计等待</div>
                            <div style="font-size: 18px; font-weight: bold;"><%= rs.getInt("estimated_wait_time") %>分钟</div>
                        </div>
                        <div>
                            <div style="font-size: 14px; color: #7f8c8d;">状态</div>
                            <div><span class="btn <%= statusClass %>" style="padding: 5px 10px;"><%= statusText %></span></div>
                        </div>
                    </div>
                    
                    <div style="display: flex; gap: 10px; margin-top: 10px;">
                        <button class="btn btn-danger" onclick="cancelQueue(<%= rs.getInt("id") %>)">取消排队</button>
                        <button class="btn" onclick="viewDetails(<%= rs.getInt("id") %>)">查看详情</button>
                    </div>
                </div>
                <%
                                }
                            }
                        } catch (SQLException e) {
                            out.println("<p>数据库错误: " + e.getMessage() + "</p>");
                        }
                    }
                %>
            </div>
            
            <!-- 个人资料 -->
            <div id="profile" class="card" style="display: none;">
                <div class="card-title">个人资料</div>
                
                <%
                    if (session.getAttribute("customer_id") == null) {
                %>
                <div style="text-align: center; padding: 40px;">
                    <p>您尚未登录，无法查看和修改个人资料</p>
                    <a href="login.jsp" class="btn btn-primary">立即登录</a>
                    <a href="register.jsp" class="btn" style="margin-left: 10px;">注册新账号</a>
                </div>
                <%
                    } else {
                %>
                <form method="post" action="updateCustomerProfile.jsp">
                    <div class="form-group">
                        <label for="profile_name">姓名</label>
                        <input type="text" id="profile_name" name="name" 
                               value="<%= session.getAttribute("customer_name") %>" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="profile_phone">手机号码</label>
                        <input type="tel" id="profile_phone" name="phone" 
                               value="<%= session.getAttribute("customer_phone") %>" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="profile_email">电子邮箱</label>
                        <input type="text" id="profile_email" name="email" 
                               value="<%= session.getAttribute("customer_email") != null ? session.getAttribute("customer_email") : "" %>">
                    </div>
                    
                    <div class="form-group">
                        <label for="notification_pref">通知偏好</label>
                        <select id="notification_pref" name="notification_pref">
                            <option value="sms" <%= "sms".equals(session.getAttribute("notification_pref")) ? "selected" : "" %>>短信通知</option>
                            <option value="app" <%= "app".equals(session.getAttribute("notification_pref")) ? "selected" : "" %>>APP通知</option>
                            <option value="both" <%= "both".equals(session.getAttribute("notification_pref")) ? "selected" : "" %>>短信和APP</option>
                        </select>
                    </div>
                    
                    <button type="submit" class="btn btn-success">保存更改</button>
                </form>
                <%
                    }
                %>
            </div>
        </div>
    </div>
    
    <script>
        // 侧边栏导航
        document.querySelectorAll('.sidebar a').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                // 更新活动链接样式
                document.querySelectorAll('.sidebar a').forEach(a => a.classList.remove('active'));
                this.classList.add('active');
                
                // 隐藏所有内容区域
                document.querySelectorAll('.content > .card').forEach(card => {
                    card.style.display = 'none';
                });
                
                // 显示选中的内容区域
                const targetId = this.getAttribute('href').substring(1);
                document.getElementById(targetId).style.display = 'block';
                
                // 如果是通过餐厅卡片跳转到预约页面
                const urlParams = new URLSearchParams(window.location.hash.substring(1));
                const restaurantId = urlParams.get('restaurant_id');
                if (targetId === 'reservation' && restaurantId) {
                    document.getElementById('queue_restaurant').value = restaurantId;
                    updateEstimatedWaitTime();
                }
            });
        });
        
        // 餐厅选择变化时更新预计等待时间
        document.getElementById('queue_restaurant').addEventListener('change', function() {
            updateEstimatedWaitTime();
        });
        
        function updateEstimatedWaitTime() {
            const restaurantSelect = document.getElementById('queue_restaurant');
            const selectedOption = restaurantSelect.options[restaurantSelect.selectedIndex];
            if (selectedOption.value) {
                // 从选项文本中提取等待时间
                const match = selectedOption.text.match(/预计等待(\d+)分钟/);
                if (match && match[1]) {
                    document.getElementById('waitTimeValue').textContent = match[1] + '分钟';
                    document.getElementById('estimatedWaitTime').style.display = 'block';
                }
            } else {
                document.getElementById('estimatedWaitTime').style.display = 'none';
            }
        }
        
        // 加入排队
        function joinQueue() {
            const restaurantId = document.getElementById('queue_restaurant').value;
            const partySize = document.getElementById('queue_party_size').value;
            const customerName = document.getElementById('customer_name').value;
            const customerPhone = document.getElementById('customer_phone').value;
            
            if (!restaurantId || !customerName || !customerPhone) {
                alert('请填写完整信息');
                return;
            }
            
            // 显示加载中
            document.getElementById('queueLoading').style.display = 'block';
            document.getElementById('queueResult').style.display = 'none';
            document.getElementById('reminderSection').style.display = 'none';
            
            // 模拟AJAX请求
            setTimeout(function() {
                document.getElementById('queueLoading').style.display = 'none';
                
                // 生成随机排队号码
                const letters = 'ABCDEFGHJKLMNPQRSTUVWXYZ';
                const randomLetter = letters[Math.floor(Math.random() * letters.length)];
                const randomNumber = Math.floor(Math.random() * 200) + 1;
                const queueNumber = randomLetter + randomNumber;
                
                document.getElementById('queueNumber').textContent = queueNumber;
                document.getElementById('queueResult').style.display = 'block';
                document.getElementById('reminderSection').style.display = 'block';
                
                // 实际项目中应该使用AJAX提交数据
                // fetch('joinQueue.jsp', {
                //     method: 'POST',
                //     body: JSON.stringify({
                //         restaurant_id: restaurantId,
                //         party_size: partySize,
                //         customer_name: customerName,
                //         customer_phone: customerPhone
                //     }),
                //     headers: {
                //         'Content-Type': 'application/json'
                //     }
                // })
                // .then(response => response.json())
                // .then(data => {
                //     // 处理返回的排队信息
                // });
            }, 1500);
        }
        
        // 设置提醒
        function setReminder() {
            const reminderTime = document.getElementById('reminder_time').value;
            const reminderMethod = document.getElementById('reminder_method').value;
            
            // 显示提醒设置成功
            document.getElementById('reminderSet').style.display = 'block';
            
            // 实际项目中应该使用AJAX提交提醒设置
            // fetch('setReminder.jsp', {
            //     method: 'POST',
            //     body: JSON.stringify({
            //         queue_id: queueId,
            //         reminder_time: reminderTime,
            //         reminder_method: reminderMethod
            //     }),
            //     headers: {
            //         'Content-Type': 'application/json'
            //     }
            // })
            // .then(response => response.json())
            // .then(data => {
            //     // 处理返回的结果
            // });
        }
        
        // 取消排队
        function cancelQueue(queueId) {
            if (confirm('确定要取消这个排队吗？')) {
                // 实际项目中应该使用AJAX取消排队
                // fetch('cancelQueue.jsp?queue_id=' + queueId)
                // .then(response => response.json())
                // .then(data => {
                //     // 刷新排队列表
                //     location.reload();
                // });
                
                alert('排队已取消');
                location.reload();
            }
        }
        
        // 查看排队详情
        function viewDetails(queueId) {
            // 实际项目中应该跳转到详情页或显示模态框
            alert('将显示排队详情，ID: ' + queueId);
        }
        
        // 页面加载时处理URL参数
        document.addEventListener('DOMContentLoaded', function() {
            const urlParams = new URLSearchParams(window.location.hash.substring(1));
            const tab = urlParams.keys().next().value;
            
            if (tab) {
                // 激活对应的标签页
                const tabLink = document.querySelector(`.sidebar a[href="#${tab}"]`);
                if (tabLink) {
                    tabLink.click();
                }
            }
        });
    </script>
</body>
</html>