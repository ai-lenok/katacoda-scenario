# Общение с базой данных

## Задание
Добавьте в поддержку базы данных

## Детальное описание задачи
1. Добавьте в файл `AddressBookRepository` поддержку реактивного общение с базой данных

<pre class="file" data-filename="/root/src/main/java/org/example/addressbook/repository/AddressBookRepository.java" data-marker="public interface AddressBookRepository {">
</pre>

2. Подключите `AddressBookRepository` в `AddressBookController`
<pre class="file" data-filename="/root/src/main/java/org/example/addressbook/controller/AddressBookController.java" data-marker="public class AddressBookController {">
</pre>

3. Запустите Unit тесты и убедитесь, что приложение собирается без ошибок

```
mvn verify
```{{execute}}