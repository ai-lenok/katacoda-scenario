Важно продумать какой каталог вы добавляете в `PATH`

## Объяснение

Теперь, все исполняемые файлы в домашней директории можно запустить из любого места

Для начал выполним команду

`cd ~`{{execute}}

`cat my-app`{{execute}}

Чтобы посмотреть содержимое `my-app`

### Добавим новый скрипт

Добавим в домашний каталог ещё один скрипт:

`echo "echo Wrong app" > cat`{{execute}}

`chmod +x cat`{{execute}}

Попробуем ещё раз вывести содержание `my-app`:

`cat my-app`{{execute}}

Получаем неожиданное сообщение

Потому что скрипт `cat` в домашней директории заменил стандартное приложение