Оператор `&>` записывает и обычный текст и ошибки из `stdout` и `stderr`

`stdout.txt`{{open}}

Запишем обычный текст в `stdout.txt`:
`echo "stdout" &> stdout.txt`{{execute}}

`stderr.txt`{{open}}

Запишем ошибку в `stderr.txt`:
`ls stderr &> stderr.txt`{{execute}}

## Способ проверки

У этого упражнения нет проверки

Когда вы нажмёте **Завершить** - упражнение закроется