Разверните Pod с приложением addressbook

## Детали

Откройте `pod.yaml`
`pod.yaml`{{open}}

1. Напишите конфигурацию Pod

- Pod name: \
  `addressbook`
- Docker-образ: \
  `nexus.local:5000/java-school/cloud/addressbook:1`
- В список labels добавьте \
  `app: addressbook`

2. Запустите Pod используя написанную конфигурацию `pod.yaml`