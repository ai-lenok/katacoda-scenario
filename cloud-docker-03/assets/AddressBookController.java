package org.example.addressbook.controller;

import org.example.addressbook.model.AddressBook;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;

@RestController
@RequestMapping("/api/v1")
public class AddressBookController {
    @GetMapping("addressbooks")
    public Flux<AddressBook> getAddressBook() {
        return Flux.empty();
    }
}
