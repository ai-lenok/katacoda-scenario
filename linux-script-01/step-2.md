Заменим команду Bash на команду Python:

<pre class="file" data-filename="script.sh" data-target="insert" data-marker="echo 'Hello world'">
print("Hello world")
</pre>

Теперь этот файл не возможно запустить с помощью команды:

`./script.sh`{{execute}}

Получаем сообщение, что Bash не знает команды `print`

Зато можно запустить скрипт с помощью Python:

`python3 script.sh`{{execute}}