Создайте ConfigMap содержащий файл

## Детали

Откройте `config-map.yaml`
`config-map.yaml`{{open}}

1. Напишите конфигурацию ConfigMap

- ConfigMap name: \
  `application-file-config`
- Добавьте файл `application.yaml` со следующим содержанием:

```text
app:
    userId: 123
    host: https://example.com
```

2. Добавьте ConfigMap в OpenShift используя написанную конфигурацию `config-map.yaml`