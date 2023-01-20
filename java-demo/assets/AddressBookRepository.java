package org.example.addressbook.repository;

import org.example.addressbook.model.AddressBook;
import org.springframework.data.domain.Pageable;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;

@Repository
public interface AddressBookRepository extends ReactiveCrudRepository<AddressBook, Long> {
    Flux<AddressBook> findAllBy(Pageable pageable);
}
