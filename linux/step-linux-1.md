## Задание

1. Вывести в консоль `Hello world`
<pre class="file" data-filename="./00.sh" data-target="insert" data-marker="## ------------->">
echo "Hello world"
</pre>

2. Найти с помощью утилит Linux, где находится приложение `python3` в системе
<pre class="file" data-filename="./01.sh" data-target="insert" data-marker="## ------------->">
which python3
</pre>

3. С помощью утилит Linux выяснить, что представляет из себя команда `ls`, чем на самом деле она является
<pre class="file" data-filename="./02.sh" data-target="insert" data-marker="## ------------->">
type ls
</pre>

4. Выведите версию ядра Linux, проверяемой системы
<pre class="file" data-filename="./03.sh" data-target="insert" data-marker="## ------------->">
uname -a
</pre>

4. В каталоге `/usr/bin/` выведите все файлы, начинающиеся с символом `s` и заканчивающиеся символом `d`. Условие: вы находитесь в другой директории, заходить в каталог `/usr/bin/` - нельзя.
<pre class="file" data-filename="./04.sh" data-target="insert" data-marker="## ------------->">
ls /usr/bin/s*d
</pre>