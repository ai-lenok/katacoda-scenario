Третья не заданная переменная окружения

**`not_set_my_var`**:
`echo ${not_set_my_var}`{{execute}}

Теперь воспользуемся оператором **`:?`**
`echo ${not_set_my_var:?message if not set}`{{execute}}

Мы увидели

**`bash: not_set_my_var: message if not set`**

Это похоже на поведение предыдущих операторов

Тут же проверим статус команды:
`echo "Status: $?"`{{execute}}

Оператор **`:?`** генерирует ошибку, если переменной нет

Теперь посмотрим на содержимое `not_set_my_var`:
`echo ${not_set_my_var}`{{execute}}

Переменная не поменяла своё значение

Проверим, какой статус будет, если задать значение переменной:
`
not_set_my_var="Text"
echo ${not_set_my_var:?message if not set}
echo "Status: $?"
`{{execute}}

Оператор **`:?`** вывел значение переменной

И вернул успешный статус выполнения