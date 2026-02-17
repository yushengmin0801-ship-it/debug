package com.example.calculator;

import org.springframework.web.bind.annotation.*;
import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*") // Allow Vue to access
public class CalculatorController {

    private List<String> history = new ArrayList<>();

    @PostMapping("/calculate")
    public CalculationResponse calculate(@RequestBody CalculationRequest request) {
        double result = 0;
        switch (request.getOperator()) {
            case "+":
                result = request.getNum1() + request.getNum2();
                break;
            case "-":
                result = request.getNum1() - request.getNum2();
                break;
            case "*":
                result = request.getNum1() * request.getNum2();
                break;
            case "/":
                if (request.getNum2() != 0) {
                    result = request.getNum1() / request.getNum2();
                } else {
                    throw new IllegalArgumentException("Cannot divide by zero");
                }
                break;
            default:
                throw new IllegalArgumentException("Invalid operator: " + request.getOperator());
        }

        // Add to history
        String entry = String.format("%s %s %s = %s", request.getNum1(), request.getOperator(), request.getNum2(), result);
        history.add(0, entry); // Add to beginning for latest first
        if (history.size() > 5) {
            history.remove(history.size() - 1);
        }

        return new CalculationResponse(result);
    }

    @GetMapping("/history")
    public List<String> getHistory() {
        return history;
    }
}
