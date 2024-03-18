Файл `/dev/random` является логическим продолжением `/dev/zero`

По всем свойствам он похож на `/dev/zero`

Но если начать его читать, то он возвращает не нули

А бесконечный поток псевдо-случайных чисел

```
dd if=/dev/random of=random1.iso bs=32 count=32
cat random1.iso
```{{execute}}

```
dd if=/dev/random of=random2.iso bs=32 count=32
cat random2.iso
```{{execute}}

Обычно этим свойством пользуются, чтобы создать какую-нибудь уникальную сущность

Например, уникальную хэш-сумму:

`dd if=/dev/random bs=512 count=1 | sha512sum`{{execute}}