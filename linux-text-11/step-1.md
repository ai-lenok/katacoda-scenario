Сравните файлы `application-test.yaml` и `application-production.yaml` между собой

## Детали

Представьте, что у вас есть два конфигурационных файла:

- `application-test.yaml` - рабочие конфигурации, которые вы активно изменяли
- `application-production.yaml` - эталонные конфигурации, использующиеся в промышленной среде

После длительной работы над `application-test.yaml` вам нужно понять

Есть ли изменения в этом файле, по сравнению с `application-production.yaml`

И если да, то какие?

Для начала посмотрите глазами на эти файлы

`application-test.yaml`{{open}}

`application-production.yaml`{{open}}

Удастся ли вам сравнить их самостоятельно?

На сколько это сложно сделать?

Теперь сравним их при помощи утилиты `diff`:

`diff application-production.yaml application-test.yaml`{{execute}}

## Способ проверки

У этого упражнения нет проверки

Когда вы нажмёте **Завершить** - упражнение закроется