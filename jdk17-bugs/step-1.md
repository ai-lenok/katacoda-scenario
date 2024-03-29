## Краткое описание

volume хранилище в docker работает в режиме read-only

## Детализация

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

## Ожидаемое поведение

Контейнер может записать файлы в volume хранилище

## Воспроизведение

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