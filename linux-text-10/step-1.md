Выведите строки отвечающие шаблону

## Детали

Откройте файл `script.sh`{{open}}

Напишите команду, которая отфильтрует только ссылки из файла `file.txt`

Пример отфильтрованного текста:

```text
lrwxrwxrwx 1 root   root          11 Mar 23 18:56 core -> /proc/kcore
lrwxrwxrwx 1 root   root          13 Mar 23 18:56 fd -> /proc/self/fd
lrwxrwxrwx 1 root   root          12 Mar 23 18:56 initctl -> /run/initctl
```

## Способ проверки

Автотест выполнит команду в `script.sh`

И проверит: полученный результат верен ожидаемому