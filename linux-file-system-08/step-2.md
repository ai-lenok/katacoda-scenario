`/dev/full` такая же "чёрная дыра", как и `/dev/null`

Повторим пример с записью и выводом содержания:

```
cat /dev/full
echo "Hello" > /dev/full
cat /dev/full
```{{execute}}

Важное отличие от `/dev/null` в том, что запись в `/dev/full` всегда приводит к ошибке:

```
echo "Hello" > /dev/full
echo "Status: $?"
```{{execute}}

Можете пользоваться этой особенностью, когда вам нужно сгенерировать ошибку:

```
echo "Hello" > /dev/full || echo "Произошла ошибка"
```{{execute}}