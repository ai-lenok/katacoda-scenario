Вызовете файл по абсолютному и сокращенному пути

## Детали

В каталоге `dir` находится файл `script.sh`

`dir/script.sh`{{open}}

Прочитаем его содержимое в терминале

## Относительный путь

Находясь в домашней директории выполните:

`cat dir/script.sh`{{execute}}

Если зайти в каталог `dir`

`cd dir`{{execute}}

То команда перестанет работать:

`cat dir/script.sh`{{execute}}

Зато будет работать другая:

`cat script.sh`{{execute}}

Потому что путь поменялся