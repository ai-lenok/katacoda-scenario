package org.example.addressbook.controller;

import org.example.addressbook.model.AddressBook;
import org.example.addressbook.repository.AddressBookRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.reactive.server.WebTestClient;

import java.time.LocalDate;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertEquals;

@SpringBootTest
@AutoConfigureMockMvc
class AddressBookControllerTest {
    @Autowired
    WebTestClient webTestClient;

    @Autowired
    AddressBookRepository repository;

    @Test
    void contextLoads() {
        assertThat(webTestClient).isNotNull();
    }

    @Test
    void testFindAll() {
        webTestClient.get()
                .uri("/api/v1/addressbook")
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .json("""
                        [{"id":-3,"firstName":"Petr","lastName":"Petrov","phone":"+79222222222","birthday":"1990-01-01"},
                        {"id":-2,"firstName":"Ivan","lastName":"Ivanov","phone":"+79111111111","birthday":"2000-01-01"},
                        {"id":-1,"firstName":"Aleksey","lastName":"Alekseev","phone":"+79000000000","birthday":"1980-01-01"}]
                        """);

    }
}