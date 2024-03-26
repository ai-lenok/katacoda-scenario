Выведите список всех пользователей в системе

## Детали

Откройте файл `script.sh`{{open}}

Напишите команду, которая отобразит файл, содержащий список всех пользователей в системе

Пример вывода:

```text
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
sshd:x:74:74:Privilege-separated SSH:/var/empty/sshd:/sbin/nologin
user:x:1000:1000:Regular user:/home/user:/bin/bash
```

## Способ проверки

Автотест выполнит команду в `script.sh`

И проверит: полученный результат верен ожидаемому