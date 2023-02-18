## 1 - Volume хранилище

### Краткое описание

volume хранилище в docker работает в режиме read-only

### Детализация

Создать volume хранилище в docker, подключить к контейнеру, попробовать туда записать данные, возникает ошибка
permission

В этой виртуальной машине неправильно работает инструкция

```yaml
volumes:
  - data-db:/var/lib/postgresql/data
```

```yaml
volumes:
  data-db:
```

### Ожидаемое поведение

Контейнер может записать файлы в volume хранилище

### Воспроизведение

Откройте `compose.yaml`
`compose.yaml`{{open}}

Выполните

`docker-compose up`{{execute}}

Должны увидеть:

```text
root-db-1  | chmod: changing permissions of '/var/lib/postgresql/data': Read-only file system
root-db-1  | chmod: changing permissions of '/var/lib/postgresql/data': Read-only file system
root-db-1  | The files belonging to this database system will be owned by user "postgres".
root-db-1  | This user must also own the server process.
root-db-1  | 
root-db-1  | The database cluster will be initialized with locale "en_US.utf8".
root-db-1  | The default database encoding has accordingly been set to "UTF8".
root-db-1  | The default text search configuration will be set to "english".
root-db-1  | 
root-db-1  | Data page checksums are disabled.
root-db-1  | 
root-db-1  | initdb: error: could not change permissions of directory "/var/lib/postgresql/data": Read-only file system
```

## 2 - Монтирование volume папки к host системе

### Краткое описание

После монтирование volume к host системе в окне «Работа с файлами» пропадают старые файлы

### Воспроизведение

Поменяйте

```yaml
volumes:
  - data-db:/var/lib/postgresql/data
```

На

```yaml
volumes:
  - ./data:/var/lib/postgresql/data
```

<pre class="file" data-filename="./compose.yaml" data-target="insert" data-marker="- data-db:/var/lib/postgresql/data">
- ./data:/var/lib/postgresql/data
</pre>

Смотрите в окно "Работа с файлами"

Выполните

`docker-compose up --detach`{{execute}}

Должны пропасть старые файлы и появиться каталог `data`

### Ожидаемое поведение

Старые файлы не пропадают

## 3 - docker-compose up не возвращает управление в терминал

### Краткое описание

Выход из docker-compose up не возвращает управление в терминал

### Как воспроизвести

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

### Ожидаемое поведение

Нажимал Ctrl+C \
Вернулся ввод \
Продолжил вводить команды

### Особенности

С обычным docker всё работает корректно
`sudo docker pull dzx912/addressbook:1`{{execute}}
`docker run dzx912/addressbook:1`{{execute}}