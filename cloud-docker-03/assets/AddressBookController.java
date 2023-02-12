package org.example.addressbook.controller;

import org.example.addressbook.model.AddressBook;
import org.example.addressbook.repository.AddressBookRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;

import java.util.Optional;

@RestController
@RequestMapping("/api/v1")
public class AddressBookController {
    @GetMapping("addressbooks")
    public Flux<AddressBook> getAddressBook() {
        return Flux.empty();
    }
}
