У оператора `;` есть особенность

Он игнорирует ошибки

Для примера создадим два раза каталог `fail_dir` и попробуем в него зайти:

```shell
cd ~
mkdir fail_dir
mkdir fail_dir
cd fail_dir
```

`cd ~; mkdir fail_dir; mkdir fail_dir; cd fail_dir`{{execute}}

В терминале можете заметить ошибку

```text
mkdir: cannot create directory ‘fail_dir’: File exists
```

Её вызывает вторая команда `mkdir fail_dir`

Потому что каталог уже существует

Но мы всё равно попадём в `fail_dir` потому что оператор

`;`

Заставляет последнюю команду `cd fail_dir` проигнорировать ошибку

