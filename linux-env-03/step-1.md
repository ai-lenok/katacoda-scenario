Обратитесь к переменным окружения используя разные операторы

## Детали

## Вывести значение по-умолчанию

`echo ${my_var}`{{execute}}
`echo ${my_var:-5}`{{execute}}
`echo ${my_var}`{{execute}}

## Записать значение, если не задано

`echo ${set_my_var}`{{execute}}
`echo ${set_my_var:=5}`{{execute}}
`echo ${set_my_var}`{{execute}}

## Вывести ошибку, если переменной нет

`echo ${not_set_my_var}`{{execute}}
`echo ${not_set_my_var:?message if not set}`{{execute}}
`echo "status: $?"`{{execute}}
`echo ${not_set_my_var}`{{execute}}

## Сообщить, если переменная существует

`echo ${check_if_set}`{{execute}}
`echo ${check_if_set:+variable set}`{{execute}}
`echo ${check_if_set}`{{execute}}
`check_if_set="10"`{{execute}}
`echo ${check_if_set:+variable set}`{{execute}}

## Способ проверки

У этого упражнения нет проверки

Когда вы нажмёте **Завершить** - упражнение закроется