## Краткое описание

После монтирование volume к host системе в окне «Работа с файлами» пропадают старые файлы

## Воспроизведение

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

## Ожидаемое поведение

Старые файлы не пропадают