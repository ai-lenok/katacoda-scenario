Перенаправьте текст

## Детали

Мы будем работать с файлами `stdout.txt` и `stderr.txt`

Сюда будем отправлять обычный вывод:
`stdout.txt`{{open}}

Сюда ошибки:
`stderr.txt`{{open}}


Для начала выведем текст в терминал:
`echo "Hello"`{{execute}}

Теперь текст, который мы вывели в терминал перенаправим в файл `stdout.txt`:
`echo "Hello" > stdout.txt`{{execute}}


`echo "World" >> stdout.txt`{{execute}}
`echo "Rewrite" > stdout.txt`{{execute}}

`ls not-exists`{{execute}}

`ls first 2> stderr.txt`{{execute}}
`ls second 2>> stderr.txt`{{execute}}
`ls rewrite 2> stderr.txt`{{execute}}

`echo "Oops" 2> stdout.txt`{{execute}}
`ls oops > stderr.txt`{{execute}}

`echo "stdout" &> stdout.txt`{{execute}}
`ls stderr &> stderr.txt`{{execute}}

## Способ проверки

У этого упражнения нет проверки

Когда вы нажмёте **Завершить** - упражнение закроется