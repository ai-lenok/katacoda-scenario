package org.example.demo.controller;

import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/api/v1")
public class DemoController {

    @GetMapping("/test")
    public Mono<String> test() {
        return Mono.just("Hello reactive world");
    }
}
