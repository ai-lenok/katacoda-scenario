## Краткое описание

Выход из docker-compose up не возвращает управление в терминал

## Как воспроизвести

Запускаем `docker-compose up`{{execute}} без `--detach`
Нажимаем Ctrl+C \
Ввод в терминал не возвращается

Если пару раз нажать на это сочетание, видим

```text
^CGracefully stopping... (press Ctrl+C again to force)
Aborting on container exit...
[+] Running 1/0
 ⠿ Container root-db-1  Stopped                                                                                                                       0.0s
^Cno container to kill
```

## Ожидаемое поведение

Нажимал Ctrl+C \
Вернулся ввод \
Продолжил вводить команды

## Особенности

С обычным docker всё работает корректно
`sudo docker pull dzx912/addressbook:1`{{execute}}
`docker run dzx912/addressbook:1`{{execute}}