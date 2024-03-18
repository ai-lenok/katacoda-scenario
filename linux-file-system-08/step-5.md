Файл `/dev/random` является логическим продолжением `/dev/zero`

По всем свойствам он похож на `/dev/zero`

Но если начать его читать, то он возвращает не нули

А бесконечный поток псевдо-случайных чисел

```
head --bytes=30 /dev/random > random1.iso
cat random1.iso
```{{execute}}

```
head --bytes=30 /dev/random > random2.iso
cat random2.iso
```{{execute}}

Обычно этим свойством пользуются, чтобы создать какую-нибудь уникальную сущность

Например, уникальную хэш-сумму:

`head --bytes=512 /dev/random | sha512sum`{{execute}}