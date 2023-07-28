Разверните Pod c labels и annotations

## Детали

Откройте `pod.yaml`
`pod.yaml`{{open}}

1. Напишите конфигурацию Pod

- Pod name: \
  `addressbook`
- Docker-образ: \
  `nexus.local:5000/java-school/cloud/addressbook:1`
- labels:
    - app: addressbook
    - environment: dev
    - release: stable
- annotations:
    - documentation: https://example.com/docs
    - dependency: postgres
    - author: user
    - email: user@mail.com

2. Запустите Pod используя написанную конфигурацию `pod.yaml`