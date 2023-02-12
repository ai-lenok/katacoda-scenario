package org.example.addressbook.model;

import org.springframework.data.annotation.Id;
import java.time.LocalDate;

public record AddressBook(@Id Long id, String firstName, String lastName, String phone, LocalDate birthday) {
    boolean hasId() {
        return id != null;
    }
}
