package com.example.springdemo.logic;


import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;

@Service
public class TxtFileReader {

    public Map<String, String> readAllTxtFiles(String folderPath) throws IOException {
        Map<String, String> fileContents = new HashMap<>();

        Files.walk(Paths.get(folderPath))
                .filter(Files::isRegularFile)
                .filter(path -> path.toString().endsWith("count.txt"))
                .forEach(path -> {
                    try {
                        String fileName = path.getFileName().toString();
                        String content = new String(Files.readAllBytes(path));
                        String name = fileName.replace("_count.txt", "");
                        fileContents.put(name, content);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                });

        return fileContents;
    }
}

