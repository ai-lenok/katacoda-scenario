## Задание

### Кратко

Разверните Pod с приложением addressbook

### Детализация

1. Напишите конфигурацию Pod

Откройте `pod.yaml`
`pod.yaml`{{open}}

- Pod name: `addressbook`
- Docker-образ: `nexus.local:5000/java-school/cloud/addressbook:1`
- В список labels добавьте

```yaml
app: addressbook
```

2. Запустите Pod используя написанную конфигурацию