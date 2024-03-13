Добьёмся, чтобы `my-app` запускался из любого каталога

## Детали

Для этого копируем `my-app` в каталог, из переменной окружения

`PATH`

В начале выведем содержание `PATH`:

`echo $PATH`{{execute}}

Один из каталогов `/usr/local/bin`

В него и будем копировать:

`sudo cp /home/ubuntu/my-app /usr/local/bin/`{{execute}}