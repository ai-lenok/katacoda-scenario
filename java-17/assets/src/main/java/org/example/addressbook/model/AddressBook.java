package org.example.addressbook.model;

import org.springframework.data.annotation.Id;

import java.time.LocalDate;
import java.util.Objects;

public record AddressBook(@Id Long id, String firstName, String lastName, String phone, LocalDate birthday) {
    boolean hasId() {
        return id != null;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        AddressBook that = (AddressBook) o;
        return Objects.equals(id, that.id)
                && Objects.equals(firstName, that.firstName)
                && Objects.equals(lastName, that.lastName)
                && Objects.equals(phone, that.phone)
                && Objects.equals(birthday, that.birthday);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, firstName, lastName, phone, birthday);
    }
}
