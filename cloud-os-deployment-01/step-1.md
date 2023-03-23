## Задание

### Кратко

Напишите скрипты стратегии развертывания Blue/Green

### Детализация

Запустите в OpenShift следующую систему:

- Deployment из 1-ой реплики с приложением `switch-blue`
    - Docker-образ приложения: \
      `dzx912/switch:blue`
- Deployment из 1-ой реплики с приложением `switch-green`
    - Docker-образ приложения: \
      `dzx912/switch:green`
- Ingress, который обращается на одно из приложений, по следующей логике:
    - Если выполнить скрипт `deploy-blue.sh`, то на запросы будет отвечать приложение `dzx912/switch:blue`
    - Если выполнить скрипт `deploy-green.sh`, то на запросы будет отвечать приложение `dzx912/switch:green`
    - Адрес в интернет:

```
http://NAMESPACE.apps.sbc-okd.pcbltools.ru
```

Где `NAMESPACE` - имя проектной области, его можно узнать с помощью команды

```
oc config view --output='json' | jq '.contexts[0].context.namespace'
```{{execute}}

### Способ проверки

Автотест выполнит скрипт `deploy-blue.sh` \
Тут же обратится на адрес `http://NAMESPACE.apps.sbc-okd.pcbltools.ru/api/v1/version` \
Должен получить ответ `blue`

Затем автотест выполнит скрипт `deploy-green.sh` \
Тут же обратится на адрес `http://NAMESPACE.apps.sbc-okd.pcbltools.ru/api/v1/version` \
Должен получить ответ `green`

### Примечание

В приложении `dzx912/switch` реализован метод `/api/v1/version` который возвращает:
- `blue` для версии `dzx912/switch:blue`
- `green` для версии `dzx912/switch:green`

Полная проверка занимает около минуты\
Наберитесь терпения, когда нажмёте кнопку "Завершить"