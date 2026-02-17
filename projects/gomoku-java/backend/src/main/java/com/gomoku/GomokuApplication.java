package com.gomoku;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import java.util.*;

@SpringBootApplication
@RestController
@CrossOrigin(origins = "*")
@RequestMapping("/api")
public class GomokuApplication {

    public static void main(String[] args) {
        SpringApplication.run(GomokuApplication.class, args);
    }

    @PostMapping("/move")
    public Map<String, Integer> getNextMove(@RequestBody Map<String, Object> payload) {
        List<List<Integer>> board = (List<List<Integer>>) payload.get("board");
        // Simple AI: find first empty spot
        int size = board.size();
        for (int r = 0; r < size; r++) {
            for (int c = 0; c < size; c++) {
                if (board.get(r).get(c) == 0) {
                    Map<String, Integer> move = new HashMap<>();
                    move.put("row", r);
                    move.put("col", c);
                    return move;
                }
            }
        }
        return null;
    }
}
