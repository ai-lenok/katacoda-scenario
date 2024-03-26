Задайте нестандартный интерпретатор скрипта

## Детали

Изначально написан стандартный Bash-скрипт

Который выводит "Hello world":

`script.sh`{{open}}

Запустить скрипт можно командной:

`./script.sh`{{execute}}

## Модификация в Python-скрипт



<pre class="file" data-filename="./script.sh" data-target="insert" data-marker="#!/usr/bin/env bash">
#!/usr/bin/env python3
</pre>

<pre class="file" data-filename="./script.sh" data-target="insert" data-marker="echo 'Hello world'">
print("Hello world")
</pre>

`./script.sh`{{execute}}

Откройте файл `script.sh`{{open}}

Напишите команду, которая

## Способ проверки

Автотест выполнит команду в `script.sh`

И проверит: полученный результат верен ожидаемому