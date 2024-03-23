Выведем ошибку в терминал:
`ls not-exists`{{execute}}

Оня связан с тем, что файл `not-exists` не существует

`stderr.txt`{{open}}

Запишем ошибку в файл:
`ls first 2> stderr.txt`{{execute}}

Добавим ещё одну ошибку:
`ls second 2>> stderr.txt`{{execute}}

Оператор `2>>` запишет текст в конец файла

Оператор `2>` сотрёт старое содержимое и запишет вместо него новый текст

Проверим:
`ls rewrite 2> stderr.txt`{{execute}}