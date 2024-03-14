Для этого выполним команду

`docker inspect cont`{{execute}}

---

Мы получили подробный отчёт

`docker inspect cont | jq .`{{execute}}

`docker inspect cont | jq .[].Config`{{execute}}

`docker inspect cont | jq .[].Config.Image`{{execute}}

## Способ проверки

Автотест выполнит команду в `script.sh`

И проверит: полученный результат верен ожидаемому