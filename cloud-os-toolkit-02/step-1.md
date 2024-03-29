## Задание

### Кратко

Установите addressbook с базой данных в OpenShift

### Детализация

Необходимо установить полноценную микросервисную систему\
На основе приложения из первого занятия

Система должна состоять из следующих элементов:

- Deployment из 2-х реплик с приложением `addressbook`
    - Имя Deployment: `addressbook`
    - Docker-образ приложения: \
      `nexus.local:5000/java-school/cloud/addressbook:1`
    - Приложение должно уметь пережить падение Pod\
      То есть, сохраненные данные в БД не должны потеряться
- StatefulSet с 1-ой репликой базы данных `PosgreSQL`
    - Имя: `db`
    - Docker-образ базы данных: \
      `bitnami/postgresql:15`
- Service, для доступа к БД
    - Адрес доступа: \
      `db.NAME_SPACE.svc.cluster.local:5432`
- Service, для доступа к `addressbook`
    - Адрес доступа: \
      `addressbook.NAME_SPACE.svc.cluster.local:9090`
    - Selector для поиска Pod: \
      `app: addressbook`

Где `NAME_SPACE` - Project / namespace, созданный под это упражнение

Команда, чтобы узнать namespace:

```
oc config view --output='json' | jq '.contexts[0].context.namespace'
```{{execute}}

Чего делать не надо:

- Настраивать Ingress для доступа к вашему приложению из интернета \
  Это общественный кластер, на котором выполняют упражнению с OpenShift \
  Все студенты СберУниверситета \
  К сожалению, нет возможности обеспечить всех уникальным доменным именем

### Как выполнять задание

В каталоге созданы пустые YAML-файлы\
В которых вы можете писать манифесты

Вы можете писать манифесты для конкретной задачи в конкретный файл\
Или собрать все в один - `all.yaml`

Не запрещается выполнить задание в Web UI

### Примечание

Это большое задание, которое подразумевает, что вы вдумчиво его выполняете

SberCode не сохраняет файлы и выключает виртуальную машину, после долгого простоя

Полная проверка занимает 2 минуты\
Наберитесь терпения, когда нажмёте кнопку "Завершить"

Рекомендуется хранить наработки на локальном компьютере, а SberCode использовать для отладки и проверки

Во время отладки не запрещается настроить Ingress, чтобы получить доступ к приложению из интернета\
Но при проверке задания, это будет считаться ошибкой