Отобразите только сообщения из журнала сервиса `cron.service`

## Детали

Откройте файл `script.sh`{{open}}

Напишите команду, которая отобразит только сообщения из журнала сервиса `cron.service`

Пример вывода:

```text
Started Regular background program processing daemon.
(CRON) INFO (pidfile fd = 3)
(CRON) INFO (Running @reboot jobs)
```

## Способ проверки

Автотест выполнит команду в `script.sh`

И проверит: полученный результат верен ожидаемому