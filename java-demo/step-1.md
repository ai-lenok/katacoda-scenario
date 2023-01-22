## Общение с базой данных

### Кратко

Добавьте поддержку базы данных

### Детализация задания

- Модель данных уже создана в классе `model.AddressBook`
  `/root/src/main/java/org/example/addressbook/model/AddressBook.java`{{open}}
- Сделана заготовка repository в интерфейсе `repository.AddressBookRepository`. Её необходимо доработать.
  `/root/src/main/java/org/example/addressbook/repository/AddressBookRepository.java`{{open}}
- Сделана заготовка controller в классе `controller.AddressBookController`. Её необходимо доработать.
  `/root/src/main/java/org/example/addressbook/controller/AddressBookController.java`{{open}}
- В каталоге `test` находится код Unit теста, который проверяет код. Добейтесь, чтобы Unit тесты проходили без ошибок.
  `/root/src/test/java/org/example/addressbook/controller/AddressBookControllerTest.java`{{open}}

Для проверки выполните команду

```
mvn verify
```{{execute}}