<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.sql.*" %>
<%!
    // 数据库连接方法
    public Connection getConnection() throws SQLException {
        String url = "jdbc:mysql://localhost:3306/people_count_db";
        String username = "admin";
        String password = "password";
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
    <title>餐厅人流量监测系统 - 管理员界面</title>
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
        .btn-danger { background-color: #e74c3c; }
        .btn-success { background-color: #2ecc71; }
        .btn-warning { background-color: #f39c12; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="text"], input[type="number"], input[type="date"], input[type="file"], select { 
            padding: 10px; 
            width: 100%; 
            border: 1px solid #ddd; 
            border-radius: 4px;
            box-sizing: border-box;
        }
        .camera-preview { 
            width: 100%; 
            height: 400px; 
            background-color: #f1f1f1; 
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px dashed #ccc;
        }
        .stats-container { 
            display: flex; 
            flex-wrap: wrap; 
            gap: 15px; 
            margin-bottom: 20px;
        }
        .stat-card { 
            flex: 1; 
            min-width: 200px; 
            background: white; 
            padding: 15px; 
            border-radius: 5px; 
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .stat-value { 
            font-size: 24px; 
            font-weight: bold; 
            color: #2c3e50;
        }
        .stat-label { 
            font-size: 14px; 
            color: #7f8c8d; 
            margin-top: 5px;
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
        <h2>餐厅人流量监测系统</h2>
        <div>
            <span style="margin-right: 15px;">欢迎, <%= session.getAttribute("username") != null ? session.getAttribute("username") : "管理员" %></span>
            <a href="logout.jsp" style="color: white; text-decoration: none;">退出</a>
        </div>
    </div>
    
    <div class="main-container">
        <div class="sidebar">
            <a href="#realtime" class="active">实时监控</a>
            <a href="#capture">图像拍摄</a>
            <a href="#detection">人体检测</a>
            <a href="#stats">数据统计</a>
            <a href="#settings">系统设置</a>
        </div>
        
        <div class="content">
            <!-- 实时监控 -->
            <div id="realtime" class="card">
                <div class="card-title">实时人数监控</div>
                
                <div class="stats-container">
                    <div class="stat-card">
                        <div class="stat-value">124</div>
                        <div class="stat-label">当前总人数</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">78%</div>
                        <div class="stat-label">座位占用率</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">15</div>
                        <div class="stat-label">今日高峰期人数</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">正常</div>
                        <div class="stat-label">拥挤状态</div>
                    </div>
                </div>
                
                <table>
                    <tr>
                        <th>区域</th>
                        <th>当前人数</th>
                        <th>最大容量</th>
                        <th>拥挤程度</th>
                        <th>最后更新时间</th>
                    </tr>
                    <%
                        try (Connection conn = getConnection();
                             Statement stmt = conn.createStatement();
                             ResultSet rs = stmt.executeQuery("SELECT * FROM realtime_stats")) {
                            while (rs.next()) {
                    %>
                    <tr>
                        <td><%= rs.getString("area_name") %></td>
                        <td><%= rs.getInt("current_count") %></td>
                        <td><%= rs.getInt("max_capacity") %></td>
                        <td><%= rs.getString("crowd_level") %></td>
                        <td><%= rs.getTimestamp("last_update") %></td>
                    </tr>
                    <%
                            }
                        } catch (SQLException e) {
                            out.println("<tr><td colspan='5'>数据库错误: " + e.getMessage() + "</td></tr>");
                        }
                    %>
                </table>
            </div>
            
            <!-- 图像拍摄 -->
            <div id="capture" class="card" style="display: none;">
                <div class="card-title">图像拍摄</div>
                
                <div class="camera-preview">
                    <p>摄像头实时画面预览区域</p>
                </div>
                
                <form method="post" action="captureImage.jsp">
                    <div class="form-group">
                        <label for="camera_location">选择摄像头位置</label>
                        <select id="camera_location" name="camera_location" required>
                            <option value="">-- 请选择 --</option>
                            <option value="入口处">入口处</option>
                            <option value="用餐区1">用餐区1</option>
                            <option value="用餐区2">用餐区2</option>
                            <option value="收银台">收银台</option>
                        </select>
                    </div>
                    
                    <button type="submit" class="btn btn-success">拍摄图像</button>
                </form>
                
                <div style="margin-top: 30px;">
                    <h3>最近拍摄的图像</h3>
                    <table>
                        <tr>
                            <th>ID</th>
                            <th>拍摄时间</th>
                            <th>摄像头位置</th>
                            <th>操作</th>
                        </tr>
                        <%
                            try (Connection conn = getConnection();
                                 Statement stmt = conn.createStatement();
                                 ResultSet rs = stmt.executeQuery("SELECT * FROM image_captures ORDER BY capture_time DESC LIMIT 5")) {
                                while (rs.next()) {
                        %>
                        <tr>
                            <td><%= rs.getInt("id") %></td>
                            <td><%= rs.getTimestamp("capture_time") %></td>
                            <td><%= rs.getString("camera_location") %></td>
                            <td>
                                <a href="viewImage.jsp?id=<%= rs.getInt("id") %>" class="btn">查看</a>
                                <a href="processImage.jsp?id=<%= rs.getInt("id") %>" class="btn btn-warning">人体检测</a>
                                <a href="deleteImage.jsp?id=<%= rs.getInt("id") %>" class="btn btn-danger">删除</a>
                            </td>
                        </tr>
                        <%
                                }
                            } catch (SQLException e) {
                                out.println("<tr><td colspan='4'>数据库错误: " + e.getMessage() + "</td></tr>");
                            }
                        %>
                    </table>
                </div>
            </div>
            
            <!-- 人体检测 -->
            <div id="detection" class="card" style="display: none;">
                <div class="card-title">人体检测</div>
                
                <div class="tab-container">
                    <div class="tab-buttons">
                        <button class="tab-button active" onclick="openTab(event, 'detect-new')">新检测</button>
                        <button class="tab-button" onclick="openTab(event, 'detect-results')">检测结果</button>
                    </div>
                    
                    <div id="detect-new" class="tab-content active">
                        <form method="post" action="processDetection.jsp" enctype="multipart/form-data">
                            <div class="form-group">
                                <label>选择检测方式</label>
                                <div>
                                    <input type="radio" id="detect-existing" name="detect-type" value="existing" checked>
                                    <label for="detect-existing">使用已拍摄图像</label>
                                    <input type="radio" id="detect-upload" name="detect-type" value="upload">
                                    <label for="detect-upload">上传新图像</label>
                                </div>
                            </div>
                            
                            <div class="form-group" id="existing-image-group">
                                <label for="image_id">选择图像</label>
                                <select id="image_id" name="image_id">
                                    <option value="">-- 请选择 --</option>
                                    <%
                                        try (Connection conn = getConnection();
                                             Statement stmt = conn.createStatement();
                                             ResultSet rs = stmt.executeQuery("SELECT id, capture_time, camera_location FROM image_captures ORDER BY capture_time DESC LIMIT 20")) {
                                            while (rs.next()) {
                                    %>
                                    <option value="<%= rs.getInt("id") %>">
                                        #<%= rs.getInt("id") %> - <%= rs.getTimestamp("capture_time") %> - <%= rs.getString("camera_location") %>
                                    </option>
                                    <%
                                            }
                                        } catch (SQLException e) {
                                            out.println("<p>数据库错误: " + e.getMessage() + "</p>");
                                        }
                                    %>
                                </select>
                            </div>
                            
                            <div class="form-group" id="upload-image-group" style="display: none;">
                                <label for="image_file">上传图像</label>
                                <input type="file" id="image_file" name="image_file" accept="image/*">
                            </div>
                            
                            <button type="submit" class="btn btn-success">开始检测</button>
                        </form>
                    </div>
                    
                    <div id="detect-results" class="tab-content">
                        <table>
                            <tr>
                                <th>检测ID</th>
                                <th>图像</th>
                                <th>检测时间</th>
                                <th>检测人数</th>
                                <th>置信度</th>
                                <th>操作</th>
                            </tr>
                            <%
                                try (Connection conn = getConnection();
                                     Statement stmt = conn.createStatement();
                                     ResultSet rs = stmt.executeQuery("SELECT d.id, d.detection_time, d.human_count, d.confidence, i.image_path " +
                                                                     "FROM human_detections d JOIN image_captures i ON d.image_id = i.id " +
                                                                     "ORDER BY d.detection_time DESC LIMIT 10")) {
                                    while (rs.next()) {
                            %>
                            <tr>
                                <td><%= rs.getInt("id") %></td>
                                <td><img src="<%= rs.getString("image_path") %>" width="50" height="50"></td>
                                <td><%= rs.getTimestamp("detection_time") %></td>
                                <td><%= rs.getInt("human_count") %></td>
                                <td><%= String.format("%.2f", rs.getDouble("confidence")) %>%</td>
                                <td>
                                    <a href="viewDetection.jsp?id=<%= rs.getInt("id") %>" class="btn">查看详情</a>
                                    <a href="deleteDetection.jsp?id=<%= rs.getInt("id") %>" class="btn btn-danger">删除</a>
                                </td>
                            </tr>
                            <%
                                    }
                                } catch (SQLException e) {
                                    out.println("<tr><td colspan='6'>数据库错误: " + e.getMessage() + "</td></tr>");
                                }
                            %>
                        </table>
                    </div>
                </div>
            </div>
            
            <!-- 数据统计 -->
            <div id="stats" class="card" style="display: none;">
                <div class="card-title">数据统计与分析</div>
                
                <form method="get" action="#stats">
                    <div style="display: flex; gap: 15px; margin-bottom: 20px;">
                        <div class="form-group" style="flex: 1;">
                            <label for="start_date">开始日期</label>
                            <input type="date" id="start_date" name="start_date" value="<%= request.getParameter("start_date") %>">
                        </div>
                        <div class="form-group" style="flex: 1;">
                            <label for="end_date">结束日期</label>
                            <input type="date" id="end_date" name="end_date" value="<%= request.getParameter("end_date") %>">
                        </div>
                        <div class="form-group" style="flex: 1;">
                            <label for="stats_area">区域</label>
                            <select id="stats_area" name="stats_area">
                                <option value="">全部区域</option>
                                <%
                                    try (Connection conn = getConnection();
                                         Statement stmt = conn.createStatement();
                                         ResultSet rs = stmt.executeQuery("SELECT DISTINCT area_name FROM historical_stats")) {
                                        while (rs.next()) {
                                            String selected = request.getParameter("stats_area") != null && 
                                                              request.getParameter("stats_area").equals(rs.getString("area_name")) ? "selected" : "";
                                %>
                                <option value="<%= rs.getString("area_name") %>" <%= selected %>><%= rs.getString("area_name") %></option>
                                <%
                                        }
                                    } catch (SQLException e) {
                                        out.println("<p>数据库错误: " + e.getMessage() + "</p>");
                                    }
                                %>
                            </select>
                        </div>
                        <div style="align-self: flex-end;">
                            <button type="submit" class="btn">查询</button>
                        </div>
                    </div>
                </form>
                
                <div style="margin: 20px 0;">
                    <canvas id="statsChart" height="300"></canvas>
                </div>
                
                <table>
                    <tr>
                        <th>日期</th>
                        <th>时间段</th>
                        <th>区域</th>
                        <th>平均人数</th>
                        <th>峰值人数</th>
                        <th>操作</th>
                    </tr>
                    <%
                        String startDate = request.getParameter("start_date");
                        String endDate = request.getParameter("end_date");
                        String area = request.getParameter("stats_area");
                        
                        String query = "SELECT * FROM historical_stats WHERE 1=1";
                        if (startDate != null && !startDate.isEmpty()) {
                            query += " AND DATE(time_period) >= '" + startDate + "'";
                        }
                        if (endDate != null && !endDate.isEmpty()) {
                            query += " AND DATE(time_period) <= '" + endDate + "'";
                        }
                        if (area != null && !area.isEmpty()) {
                            query += " AND area_name = '" + area + "'";
                        }
                        query += " ORDER BY time_period DESC LIMIT 20";
                        
                        try (Connection conn = getConnection();
                             Statement stmt = conn.createStatement();
                             ResultSet rs = stmt.executeQuery(query)) {
                            while (rs.next()) {
                    %>
                    <tr>
                        <td><%= rs.getDate("time_period") %></td>
                        <td><%= rs.getTime("time_period") %></td>
                        <td><%= rs.getString("area_name") %></td>
                        <td><%= rs.getInt("average_count") %></td>
                        <td><%= rs.getInt("peak_count") %></td>
                        <td>
                            <a href="exportData.jsp?id=<%= rs.getInt("id") %>" class="btn">导出</a>
                        </td>
                    </tr>
                    <%
                            }
                        } catch (SQLException e) {
                            out.println("<tr><td colspan='6'>数据库错误: " + e.getMessage() + "</td></tr>");
                        }
                    %>
                </table>
            </div>
            
            <!-- 系统设置 -->
            <div id="settings" class="card" style="display: none;">
                <div class="card-title">系统设置</div>
                
                <form method="post" action="saveSettings.jsp">
                    <div class="form-group">
                        <label for="system_name">系统名称</label>
                        <input type="text" id="system_name" name="system_name" value="餐厅人流量监测系统">
                    </div>
                    
                    <div class="form-group">
                        <label for="data_retention">数据保留天数</label>
                        <input type="number" id="data_retention" name="data_retention" value="30" min="1">
                    </div>
                    
                    <div class="form-group">
                        <label for="alert_threshold">拥挤警报阈值(%)</label>
                        <input type="number" id="alert_threshold" name="alert_threshold" value="80" min="1" max="100">
                    </div>
                    
                    <div class="form-group">
                        <label for="camera_settings">摄像头设置</label>
                        <select id="camera_settings" name="camera_settings">
                            <option value="auto">自动调整</option>
                            <option value="manual">手动设置</option>
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
            });
        });
        
        // 标签页切换
        function openTab(evt, tabName) {
            const tabContents = document.getElementsByClassName("tab-content");
            for (let i = 0; i < tabContents.length; i++) {
                tabContents[i].classList.remove("active");
            }
            
            const tabButtons = document.getElementsByClassName("tab-button");
            for (let i = 0; i < tabButtons.length; i++) {
                tabButtons[i].classList.remove("active");
            }
            
            document.getElementById(tabName).classList.add("active");
            evt.currentTarget.classList.add("active");
        }
        
        // 检测方式切换
        document.querySelectorAll('input[name="detect-type"]').forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.value === 'existing') {
                    document.getElementById('existing-image-group').style.display = 'block';
                    document.getElementById('upload-image-group').style.display = 'none';
                } else {
                    document.getElementById('existing-image-group').style.display = 'none';
                    document.getElementById('upload-image-group').style.display = 'block';
                }
            });
        });
        
        // 初始化图表 (实际项目中应该使用Chart.js等库)
        document.addEventListener('DOMContentLoaded', function() {
            const ctx = document.getElementById('statsChart').getContext('2d');
            // 这里应该有实际的图表初始化代码
            console.log('图表初始化位置');
        });
    </script>
</body>
</html>