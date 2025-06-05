<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.sql.*" %>
<%!
    // 数据库连接方法
    public Connection getConnection() throws SQLException {
        String url = "jdbc:mysql://localhost:3306/restaurant_management_db";
        String username = "manager";
        String password = "manager123";
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
    <title>餐厅人流量监测系统 - 经理界面</title>
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
        table { 
            width: 100%; 
            border-collapse: collapse; 
            margin-top: 10px;
        }
        th, td { 
            border: 1px solid #ddd; 
            padding: 12px; 
            text-align: left; 
        }
        th { 
            background-color: #f8f9fa; 
            font-weight: bold;
        }
        tr:nth-child(even) { background-color: #f9f9f9; }
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
        input[type="text"], input[type="number"], input[type="date"], select { 
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
        .restaurant-image {
            width: 100%;
            height: 180px;
            background-color: #f1f1f1;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }
        .restaurant-image img {
            max-width: 100%;
            max-height: 100%;
            object-fit: cover;
        }
        .prediction-container {
            margin-top: 30px;
            text-align: center;
        }
        .prediction-image {
            max-width: 100%;
            margin-top: 20px;
            border: 1px solid #ddd;
            display: none;
        }
        .loading {
            display: none;
            margin: 20px 0;
            text-align: center;
            color: #7f8c8d;
        }
    </style>
</head>
<body>
    <div class="header">
        <h2>餐厅人流量监测系统 - 经理面板</h2>
        <div>
            <span style="margin-right: 15px;">欢迎, <%= session.getAttribute("manager_name") != null ? session.getAttribute("manager_name") : "经理" %></span>
            <a href="logout.jsp" style="color: white; text-decoration: none;">退出</a>
        </div>
    </div>
    
    <div class="main-container">
        <div class="sidebar">
            <a href="#restaurants" class="active">餐厅管理</a>
            <a href="#prediction">人流量预测</a>
            <a href="#reports">分析报告</a>
            <a href="#settings">个人设置</a>
        </div>
        
        <div class="content">
            <!-- 餐厅管理 -->
            <div id="restaurants" class="card">
                <div class="card-title">管理的餐厅</div>
                
                <form method="get" action="#restaurants">
                    <div style="display: flex; gap: 15px;">
                        <div class="form-group" style="flex: 1;">
                            <label for="search_name">餐厅名称</label>
                            <input type="text" id="search_name" name="search_name" placeholder="输入餐厅名称" value="<%= request.getParameter("search_name") != null ? request.getParameter("search_name") : "" %>">
                        </div>
                        <div class="form-group" style="flex: 1;">
                            <label for="search_location">位置</label>
                            <input type="text" id="search_location" name="search_location" placeholder="输入位置" value="<%= request.getParameter("search_location") != null ? request.getParameter("search_location") : "" %>">
                        </div>
                        <div style="align-self: flex-end;">
                            <button type="submit" class="btn btn-primary">搜索</button>
                        </div>
                    </div>
                </form>
                
                <div class="restaurant-grid">
                    <%
                        String searchName = request.getParameter("search_name");
                        String searchLocation = request.getParameter("search_location");
                        
                        String query = "SELECT r.id, r.name, r.location, r.image_path, " +
                                      "(SELECT COUNT(*) FROM foot_traffic WHERE restaurant_id = r.id AND DATE(record_time) = CURDATE()) AS today_count, " +
                                      "(SELECT COUNT(*) FROM foot_traffic WHERE restaurant_id = r.id AND DATE(record_time) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)) AS yesterday_count " +
                                      "FROM restaurants r " +
                                      "JOIN manager_restaurants mr ON r.id = mr.restaurant_id " +
                                      "WHERE mr.manager_id = ?";
                        
                        if (searchName != null && !searchName.isEmpty()) {
                            query += " AND r.name LIKE '%" + searchName + "%'";
                        }
                        if (searchLocation != null && !searchLocation.isEmpty()) {
                            query += " AND r.location LIKE '%" + searchLocation + "%'";
                        }
                        
                        try (Connection conn = getConnection();
                             PreparedStatement pstmt = conn.prepareStatement(query)) {
                            
                            // 假设经理ID存储在session中
                            pstmt.setInt(1, session.getAttribute("manager_id") != null ? (Integer) session.getAttribute("manager_id") : 1);
                            
                            ResultSet rs = pstmt.executeQuery();
                            while (rs.next()) {
                    %>
                    <div class="restaurant-card">
                        <div class="restaurant-name"><%= rs.getString("name") %></div>
                        <div class="restaurant-location"><%= rs.getString("location") %></div>
                        
                        <div class="restaurant-image">
                            <%
                                String imagePath = rs.getString("image_path");
                                if (imagePath != null && !imagePath.isEmpty()) {
                            %>
                            <img src="<%= imagePath %>" alt="<%= rs.getString("name") %>">
                            <%
                                } else {
                            %>
                            <p>暂无餐厅图片</p>
                            <%
                                }
                            %>
                        </div>
                        
                        <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                            <div>
                                <small>今日客流: <strong><%= rs.getInt("today_count") %></strong></small>
                            </div>
                            <div>
                                <small>昨日客流: <strong><%= rs.getInt("yesterday_count") %></strong></small>
                            </div>
                        </div>
                        
                        <div style="margin-top: 15px; display: flex; gap: 10px;">
                            <a href="restaurant_detail.jsp?id=<%= rs.getInt("id") %>" class="btn btn-primary">详情</a>
                            <a href="#prediction?restaurant_id=<%= rs.getInt("id") %>" class="btn btn-warning">预测客流</a>
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
            
            <!-- 人流量预测 -->
            <div id="prediction" class="card" style="display: none;">
                <div class="card-title">人流量预测</div>
                
                <form id="predictionForm" method="post">
                    <div style="display: flex; gap: 15px;">
                        <div class="form-group" style="flex: 1;">
                            <label for="prediction_restaurant">选择餐厅</label>
                            <select id="prediction_restaurant" name="restaurant_id" required>
                                <option value="">-- 请选择餐厅 --</option>
                                <%
                                    String restaurantQuery = "SELECT r.id, r.name FROM restaurants r " +
                                                           "JOIN manager_restaurants mr ON r.id = mr.restaurant_id " +
                                                           "WHERE mr.manager_id = ? " +
                                                           "ORDER BY r.name";
                                    
                                    try (Connection conn = getConnection();
                                         PreparedStatement pstmt = conn.prepareStatement(restaurantQuery)) {
                                        
                                        pstmt.setInt(1, session.getAttribute("manager_id") != null ? (Integer) session.getAttribute("manager_id") : 1);
                                        ResultSet rs = pstmt.executeQuery();
                                        
                                        String selectedRestaurantId = request.getParameter("restaurant_id");
                                        
                                        while (rs.next()) {
                                            String selected = selectedRestaurantId != null && selectedRestaurantId.equals(rs.getString("id")) ? "selected" : "";
                                %>
                                <option value="<%= rs.getString("id") %>" <%= selected %>><%= rs.getString("name") %></option>
                                <%
                                        }
                                    } catch (SQLException e) {
                                        out.println("<p>数据库错误: " + e.getMessage() + "</p>");
                                    }
                                %>
                            </select>
                        </div>
                        <div class="form-group" style="flex: 1;">
                            <label for="prediction_days">预测天数</label>
                            <select id="prediction_days" name="days" required>
                                <option value="7">未来7天</option>
                                <option value="14">未来14天</option>
                                <option value="30">未来30天</option>
                            </select>
                        </div>
                        <div style="align-self: flex-end;">
                            <button type="button" onclick="generatePrediction()" class="btn btn-success">生成预测</button>
                        </div>
                    </div>
                </form>
                
                <div id="predictionLoading" class="loading">
                    <p>正在生成预测数据，请稍候...</p>
                </div>
                
                <div class="prediction-container">
                    <img id="predictionImage" class="prediction-image" src="" alt="人流量预测图">
                    
                    <div id="predictionResult" style="margin-top: 20px; display: none;">
                        <h3>预测结果分析</h3>
                        <table>
                            <tr>
                                <th>日期</th>
                                <th>预测客流量</th>
                                <th>相比上周</th>
                                <th>建议准备</th>
                            </tr>
                            <tr>
                                <td>2023-06-01</td>
                                <td>320人</td>
                                <td><span style="color:green">↑15%</span></td>
                                <td>增加2名服务员</td>
                            </tr>
                            <tr>
                                <td>2023-06-02</td>
                                <td>280人</td>
                                <td><span style="color:red">↓5%</span></td>
                                <td>正常准备</td>
                            </tr>
                            <!-- 更多预测数据行 -->
                        </table>
                    </div>
                </div>
            </div>
            
            <!-- 分析报告 -->
            <div id="reports" class="card" style="display: none;">
                <div class="card-title">分析报告</div>
                
                <div style="margin-bottom: 20px;">
                    <div class="form-group">
                        <label for="report_type">报告类型</label>
                        <select id="report_type" name="report_type">
                            <option value="weekly">周报</option>
                            <option value="monthly">月报</option>
                            <option value="quarterly">季报</option>
                            <option value="custom">自定义</option>
                        </select>
                    </div>
                    
                    <div id="customDateRange" style="display: none; margin-top: 15px;">
                        <div style="display: flex; gap: 15px;">
                            <div class="form-group" style="flex: 1;">
                                <label for="start_date">开始日期</label>
                                <input type="date" id="start_date" name="start_date">
                            </div>
                            <div class="form-group" style="flex: 1;">
                                <label for="end_date">结束日期</label>
                                <input type="date" id="end_date" name="end_date">
                            </div>
                        </div>
                    </div>
                    
                    <button type="button" onclick="generateReport()" class="btn btn-primary">生成报告</button>
                </div>
                
                <div id="reportContent" style="display: none;">
                    <h3>餐厅客流分析报告</h3>
                    <div style="margin: 20px 0;">
                        <canvas id="reportChart" height="300"></canvas>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <h4>关键指标</h4>
                        <div style="display: flex; gap: 15px; flex-wrap: wrap;">
                            <div style="flex: 1; min-width: 200px; background: #f8f9fa; padding: 15px; border-radius: 5px;">
                                <div style="font-size: 24px; font-weight: bold; color: #2c3e50;">1,245</div>
                                <div style="font-size: 14px; color: #7f8c8d;">总客流量</div>
                            </div>
                            <div style="flex: 1; min-width: 200px; background: #f8f9fa; padding: 15px; border-radius: 5px;">
                                <div style="font-size: 24px; font-weight: bold; color: #2c3e50;">178</div>
                                <div style="font-size: 14px; color: #7f8c8d;">日均客流量</div>
                            </div>
                            <div style="flex: 1; min-width: 200px; background: #f8f9fa; padding: 15px; border-radius: 5px;">
                                <div style="font-size: 24px; font-weight: bold; color: #2c3e50;">12:30-13:30</div>
                                <div style="font-size: 14px; color: #7f8c8d;">客流高峰时段</div>
                            </div>
                            <div style="flex: 1; min-width: 200px; background: #f8f9fa; padding: 15px; border-radius: 5px;">
                                <div style="font-size: 24px; font-weight: bold; color: #2c3e50;">15%</div>
                                <div style="font-size: 14px; color: #7f8c8d;">周同比增长</div>
                            </div>
                        </div>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <h4>各餐厅表现</h4>
                        <table>
                            <tr>
                                <th>餐厅名称</th>
                                <th>客流量</th>
                                <th>同比增长</th>
                                <th>座位利用率</th>
                                <th>评分</th>
                            </tr>
                            <tr>
                                <td>中关村分店</td>
                                <td>356</td>
                                <td><span style="color:green">↑22%</span></td>
                                <td>78%</td>
                                <td>4.8</td>
                            </tr>
                            <tr>
                                <td>朝阳门店</td>
                                <td>298</td>
                                <td><span style="color:green">↑8%</span></td>
                                <td>65%</td>
                                <td>4.6</td>
                            </tr>
                            <!-- 更多餐厅数据行 -->
                        </table>
                    </div>
                    
                    <div style="margin-top: 20px;">
                        <button class="btn btn-primary">下载PDF报告</button>
                        <button class="btn btn-success">发送到邮箱</button>
                    </div>
                </div>
            </div>
            
            <!-- 个人设置 -->
            <div id="settings" class="card" style="display: none;">
                <div class="card-title">个人设置</div>
                
                <form method="post" action="updateManagerSettings.jsp">
                    <div class="form-group">
                        <label for="manager_name">姓名</label>
                        <input type="text" id="manager_name" name="manager_name" value="<%= session.getAttribute("manager_name") != null ? session.getAttribute("manager_name") : "" %>" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="manager_email">电子邮箱</label>
                        <input type="text" id="manager_email" name="manager_email" value="<%= session.getAttribute("manager_email") != null ? session.getAttribute("manager_email") : "" %>" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="manager_phone">联系电话</label>
                        <input type="text" id="manager_phone" name="manager_phone" value="<%= session.getAttribute("manager_phone") != null ? session.getAttribute("manager_phone") : "" %>">
                    </div>
                    
                    <div class="form-group">
                        <label for="notification_pref">通知偏好</label>
                        <select id="notification_pref" name="notification_pref">
                            <option value="email" <%= "email".equals(session.getAttribute("notification_pref")) ? "selected" : "" %>>电子邮件</option>
                            <option value="sms" <%= "sms".equals(session.getAttribute("notification_pref")) ? "selected" : "" %>>短信</option>
                            <option value="both" <%= "both".equals(session.getAttribute("notification_pref")) ? "selected" : "" %>>两者</option>
                        </select>
                    </div>
                    
                    <button type="submit" class="btn btn-success">保存设置</button>
                </form>
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
                
                // 如果是通过餐厅卡片跳转到预测页面
                const urlParams = new URLSearchParams(window.location.search);
                const restaurantId = urlParams.get('restaurant_id');
                if (targetId === 'prediction' && restaurantId) {
                    document.getElementById('prediction_restaurant').value = restaurantId;
                }
            });
        });
        
        // 报告类型选择
        document.getElementById('report_type').addEventListener('change', function() {
            const customDateRange = document.getElementById('customDateRange');
            if (this.value === 'custom') {
                customDateRange.style.display = 'block';
            } else {
                customDateRange.style.display = 'none';
            }
        });
        
        // 生成预测
        function generatePrediction() {
            const restaurantId = document.getElementById('prediction_restaurant').value;
            const days = document.getElementById('prediction_days').value;
            
            if (!restaurantId) {
                alert('请选择餐厅');
                return;
            }
            
            // 显示加载中
            document.getElementById('predictionLoading').style.display = 'block';
            document.getElementById('predictionImage').style.display = 'none';
            document.getElementById('predictionResult').style.display = 'none';
            
            // 模拟AJAX请求
            setTimeout(function() {
                document.getElementById('predictionLoading').style.display = 'none';
                
                // 这里应该是从服务器获取的预测图像
                document.getElementById('predictionImage').src = 'images/prediction_sample.png';
                document.getElementById('predictionImage').style.display = 'block';
                document.getElementById('predictionResult').style.display = 'block';
                
                // 实际项目中应该使用AJAX获取真实数据
                // fetch('generatePrediction.jsp?restaurant_id=' + restaurantId + '&days=' + days)
                //   .then(response => response.json())
                //   .then(data => {
                //       // 处理返回的预测数据
                //   });
            }, 1500);
        }
        
        // 生成报告
        function generateReport() {
            const reportType = document.getElementById('report_type').value;
            let startDate, endDate;
            
            if (reportType === 'custom') {
                startDate = document.getElementById('start_date').value;
                endDate = document.getElementById('end_date').value;
                
                if (!startDate || !endDate) {
                    alert('请选择日期范围');
                    return;
                }
            }
            
            // 显示报告内容
            document.getElementById('reportContent').style.display = 'block';
            
            // 实际项目中应该使用AJAX获取报告数据
            // 并初始化图表等
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