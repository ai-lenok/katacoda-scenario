Отобразите подробную информацию об IP адресе рабочей машины

## Детали

Откройте файл `script.sh`{{open}}

Напишите команду, которая отобразит подробную информацию об IP адресе рабочей машины

Формат вывода:

```text
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0@if1983: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 00:16:3e:49:94:91 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.35.215.41/24 brd 10.35.215.255 scope global dynamic eth0
       valid_lft 3348sec preferred_lft 3348sec
    inet6 fe80::216:3eff:fe49:9491/64 scope link 
       valid_lft forever preferred_lft forever
```

## Способ проверки

Автотест выполнит команду в `script.sh`

И проверит: полученный результат верен ожидаемому