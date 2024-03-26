Задайте нестандартный интерпретатор скрипта

## Детали

`script.sh`{{open}}

`./script.sh`{{execute}}

<pre class="file" data-filename="./script.sh" data-target="insert" data-marker="#!/usr/bin/env bash">
#!/usr/bin/env python3
</pre>

<pre class="file" data-filename="./script.sh" data-target="insert" data-marker="# echo 'Hello world'">
print("Hello world")
</pre>

`./script.sh`{{execute}}

Откройте файл `script.sh`{{open}}

Напишите команду, которая

## Способ проверки

Автотест выполнит команду в `script.sh`

И проверит: полученный результат верен ожидаемому