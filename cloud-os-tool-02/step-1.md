Разверните Pod с приложением busybox

## Детали

Откройте `pod.yaml`
`pod.yaml`{{open}}

1. Напишите конфигурацию Pod

- Pod name: \
  `addressbook`
- Docker-образ: \
  `nexus.local:5000/java-school/cloud/addressbook:1`
- Откройте порт 8080

2. Запустите Pod используя написанную конфигурацию `pod.yaml`