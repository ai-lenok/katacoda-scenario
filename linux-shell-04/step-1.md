Напишите цепочку команд, где вторая команда выполняется, если первая успешная

## Детали

Представим, что мы хотим сделать backup файла

И после этого совершить операцию, которая перезатрёт оригинал

Например:

```shell
cp good-bye.txt backup/good-bye.txt
echo "Good bye" > good-bye.txt
```

Для начал посмотрите старое содержание файла

`good-bye.txt`{{open}}

А теперь выполните команду:

`cp good-bye.txt backup/good-bye.txt; echo "Good bye" > good-bye.txt`{{execute}}