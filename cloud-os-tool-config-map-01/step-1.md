Создайте ConfigMap

## Детали

Откройте `config-map.yaml`
`config-map.yaml`{{open}}

1. Напишите конфигурацию ConfigMap

- ConfigMap name: \
  `open-config`
- Добавьте данные:
  - APP_USER_ID: 123
  - APP_HOST: https://example.com

2. Добавьте ConfigMap в OpenShift используя написанную конфигурацию `config-map.yaml`