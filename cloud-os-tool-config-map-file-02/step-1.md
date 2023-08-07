Примонтируйте файл из ConfigMap

## Детали

В OpenShift уже установлен ConfigMap, который вы сделали в предыдущем упражнении

Откройте `deployment.yaml`
`deployment.yaml`{{open}}

1. Напишите конфигурацию Deployment

- Deployment name: \
  `addressbook`
- Docker-образ: \
  `nexus.local:5000/java-school/cloud/addressbook:1`
- selector:
    - app: addressbook
- Примонтируйте файл `application.yaml` из ConfigMap `application-file-config`:
  - Имя volume: `deployment-volume`
  - Каталог монтирования: `/app/config/`

2. Запустите Deployment используя написанную конфигурацию `deployment.yaml`