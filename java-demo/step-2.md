# Общение с базой данных

## Задание

Добавьте в поддержку базы данных

## Решение

1. Добавьте в файл `AddressBookRepository` поддержку реактивного общение с базой данных

<pre class="file" data-filename="./src/main/java/org/example/addressbook/repository/AddressBookRepository.java" data-target="insert" data-marker="public interface AddressBookRepository {">
public interface AddressBookRepository extends ReactiveCrudRepository<AddressBook, Long> {
</pre>

2. Подключите `AddressBookRepository` в `AddressBookController`

<pre class="file" data-filename="./src/main/java/org/example/addressbook/controller/AddressBookController.java" data-target="insert" data-marker="    // ------------->">
final AddressBookRepository repository;

    @Autowired
    public AddressBookController(AddressBookRepository repository) {
        this.repository = repository;
    }
</pre>

3. Перепишите вывод в методе `AddressBookController::getAddressBook`

<pre class="file" data-filename="./src/main/java/org/example/addressbook/controller/AddressBookController.java" data-target="insert" data-marker="return Flux.empty();">
return repository.findAll();
</pre>

5. Запустите Unit тесты и убедитесь, что приложение собирается без ошибок

```
mvn verify
```{{execute}}