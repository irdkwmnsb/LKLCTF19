# ppc-mining (2 CSA)

## Условие
Старый добрый банк как никогда нуждается в вычислительных мощностях, поэтому запускает программу 
распределенных вычислений *"Advanced Sausage Computing 2"* и просит всех добровольцев помочь в 
тестировании. Вам нужно намайнить 1 LKLCoin, для этого решайте математические примеры. Ваш человек в 
банке уже знает, как передать Вам новые секретные данные с помощью этого метода.

Примечние: все числа целые, в том числе и результат.

`nc <server_hostname> <server_port>`

## Решение
Читаем из сокета до появления `TASK:`, потом eval-им остаток строки (см. `solve.py`). ~~Либо ручками
подключаемся по netcat'у с открытым питоновским шеллом. Copy-pase-eval и готово.~~ Добавлен таймаут,
ручками теперь сложновато, но всё-таки возможно

## Флаг
`LKLCTF{R3VeRs3_oF_2CsA_i5_AsC1i_2be0ac50_a104b017}`
