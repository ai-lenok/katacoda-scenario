package org.example.addressbook.controller;

import org.example.addressbook.model.AddressBook;
import org.example.addressbook.repository.AddressBookRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.Optional;

@RestController
@RequestMapping("/api/v1")
public class AddressBookController {
    private static final Logger logger = LoggerFactory.getLogger(AddressBookController.class);
    final AddressBookRepository repository;

    @Autowired
    public AddressBookController(AddressBookRepository repository) {
        this.repository = repository;
    }

    @GetMapping("addressbooks")
    public Flux<AddressBook> getAddressBook(@RequestParam("page") Optional<Integer> pageOpt,
                                            @RequestParam("size") Optional<Integer> sizeOpt) {
        final Integer page = pageOpt.orElse(0);
        final Integer size = sizeOpt.orElse(100);
        Integer.MAX_VALUE
        logger.info("getAddressBook, page: {}, size: {}", page, size);


        return repository.findAllBy(PageRequest.of(page, size));
    }

    @PostMapping("addressbook")
    public Mono<AddressBook> save(@RequestBody AddressBook addressBook) {
        logger.info("Save {}", addressBook);
        return repository.save(addressBook);
    }
}
