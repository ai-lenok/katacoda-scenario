Объявите переменные окружения в Deployment

## Детали

Откройте `deployment.yaml`
`deployment.yaml`{{open}}

1. Напишите конфигурацию Deployment

- Deployment name: \
  `addressbook`
- Docker-образ: \
  `nexus.local:5000/java-school/cloud/addressbook:1`
- selector:
  - app: addressbook
- Добавьте переменные окружения с помощью секции `env`:
  - APP_USER_ID: "123"
  - APP_HOST: https://example.com

2. Запустите Deployment используя написанную конфигурацию `deployment.yaml`