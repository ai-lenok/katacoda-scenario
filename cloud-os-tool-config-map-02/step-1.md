Подключите ConfigMap с помощью envFrom

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
- Подключите с помощью `envFrom` всё содержимое ConfigMap `open-config`

2. Запустите Deployment используя написанную конфигурацию `deployment.yaml`