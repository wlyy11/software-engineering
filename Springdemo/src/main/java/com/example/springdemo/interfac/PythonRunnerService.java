package com.example.springdemo.interfac;

import org.springframework.stereotype.Service;
import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

@Service
public class PythonRunnerService {

    // 配置化路径（可在application.properties中设置）
    private static final String PYTHON_PATH = "C:\\Users\\wlyy\\.conda\\envs\\pytorch\\python.exe";
    private static final String SCRIPT_PATH = "E:/study/software_engineering/code/yolov5/detect.py";
    private static final int TIMEOUT_SECONDS = 500; // 执行超时时间

    public String runPythonScript(String input) {
        try {
            // 1. 验证Python路径
            File pythonExe = new File(PYTHON_PATH);
            if (!pythonExe.exists()) {
                throw new FileNotFoundException("Python解释器不存在: " + PYTHON_PATH);
            }

            // 2. 验证脚本路径
            File scriptFile = new File(SCRIPT_PATH);
            if (!scriptFile.exists()) {
                throw new FileNotFoundException("Python脚本不存在: " + SCRIPT_PATH);
            }

            // 3. 构建命令
            List<String> command = new ArrayList<>();
            command.add(pythonExe.getAbsolutePath());
            command.add(scriptFile.getAbsolutePath());
            if (input != null && !input.trim().isEmpty()) {
                command.add(input);
            }

            // 4. 创建进程构建器
            ProcessBuilder pb = new ProcessBuilder(command);
            pb.redirectErrorStream(true); // 合并错误流

            // 5. 设置工作目录（重要！解决脚本中的相对路径问题）
            pb.directory(scriptFile.getParentFile());

            // 6. 添加环境诊断日志
            System.out.println("执行命令: " + String.join(" ", command));
            System.out.println("工作目录: " + pb.directory().getAbsolutePath());

            // 7. 启动进程并处理输出
            Process process = pb.start();

            // 8. 使用CompletableFuture处理超时
            boolean finished = process.waitFor(TIMEOUT_SECONDS, TimeUnit.SECONDS);
            if (!finished) {
                process.destroy();
                throw new RuntimeException("Python脚本执行超时 (" + TIMEOUT_SECONDS + "秒)");
            }

            // 9. 读取输出
            StringBuilder output = new StringBuilder();
            try (BufferedReader reader = new BufferedReader(
                    new InputStreamReader(process.getInputStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    output.append(line).append("\n");
                }
            }

            // 10. 检查退出码
            int exitCode = process.exitValue();
            if (exitCode != 0) {
                throw new RuntimeException("Python脚本异常退出 (代码: " + exitCode + ")\n输出:\n" + output);
            }

            return output.toString().trim();

        } catch (Exception e) {
            // 11. 包装异常并添加诊断信息
            throw new RuntimeException("执行Python脚本时出错: " + e.getMessage(), e);
        }
    }
}