# Сборка

$ make

Результат в файле ./rsa

# Решение

$ gdb ./rsa
(gdb) run
...wait a bit...
^C
(gdb) p $pc+=2
(gdb) cont
LKLCTF{wh47_4_s1up1d_pr0t3ct1on}
[Inferior 1 exited normally]
(gdb)
