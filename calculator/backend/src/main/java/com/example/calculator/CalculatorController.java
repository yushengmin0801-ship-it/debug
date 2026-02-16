package com.example.calculator;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class CalculatorController {

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
        return new CalculationResponse(result);
    }
}
