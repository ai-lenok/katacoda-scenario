Для этого выполним команду

`docker inspect cont`{{execute}}

Мы получили подробный отчёт

В нём слишком много информации

Чтобы её отфильтровать воспользуемся утилитой `jq`

Передадим весь вывод на утилиту `jq`:

`docker inspect cont | jq .`{{execute}}

Теперь можем написать шаблон фильтрации

Посмотрим на секцию `Config`:

`docker inspect cont | jq .[].Config`{{execute}}

Или посмотрим имя образа из которого запустили контейнер:

`docker inspect cont | jq .[].Config.Image`{{execute}}

## Способ проверки

У этого упражнения нет проверки

Когда вы нажмёте **Завершить** - упражнение закроется