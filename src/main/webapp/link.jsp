<%@ page import="java.sql.*" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>阿里云SQL Server连接测试</title>
    <style>
        table { border-collapse: collapse; width: 80%; margin: 20px auto; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .error { color: red; }
    </style>
</head>
<body>
    <h2 style="text-align: center;">数据库连接测试</h2>
    
    <%
        Connection conn = null;
        Statement stmt = null;
        ResultSet rs = null;
        
        try {
            // 1. 加载驱动
            Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
            
            // 2. 创建连接
            String serverName = "rm-7xv5w1y9xo5ca79zx6o.sqlserver.rds.aliyuncs.com";
            String port = "3433";
            String dbName = "testdb"; // 请替换为实际数据库名
            String user = "user1";
            String password = "123456test!";
            
            String connectionUrl = "jdbc:sqlserver://" + serverName + ":" + port + ";" 
                                + "databaseName=" + dbName + ";"
                                + "user=" + user + ";"
                                + "password=" + password + ";"
                                + "encrypt=true;"
                                + "trustServerCertificate=true;"
                                + "loginTimeout=30;";
            
            conn = DriverManager.getConnection(connectionUrl);
            
            // 3. 测试查询
            stmt = conn.createStatement();
            String testQuery = "SELECT * FROM test_table"; // 查询所有表名
            rs = stmt.executeQuery(testQuery);
    %>
    
    <table>
        <tr>
            <th>数据库中的表名</th>
        </tr>
        <% while(rs.next()) { %>
            <tr>
                <td><%= rs.getString("name") %></td>
            </tr>
        <% } %>
    </table>
    
    <%
        } catch (ClassNotFoundException e) {
    %>
        <p class="error">错误: JDBC驱动未找到，请确保mssql-jdbc驱动已添加到项目中</p>
    <%
            e.printStackTrace();
        } catch (SQLException e) {
    %>
        <p class="error">错误: 数据库连接失败 - <%= e.getMessage() %></p>
    <%
            e.printStackTrace();
        } finally {
            // 4. 关闭资源
            if (rs != null) try { rs.close(); } catch (SQLException e) {}
            if (stmt != null) try { stmt.close(); } catch (SQLException e) {}
            if (conn != null) try { conn.close(); } catch (SQLException e) {}
        }
    %>
</body>
</html>
