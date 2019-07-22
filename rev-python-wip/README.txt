# Решение

Исходно питоновский файл выглядит так:

exec(__import__('base64').b64decode(<some_string>))

Заменим exec на print и запустим. Получим следующий код:

print(lambda i:("Correct"if type(lambda:None)(i,{})(i,ord,raw_input("Flag: "))else "Incorrect"))(__import__('marshal').loads(<some_other_string>))

В отформатированном виде этот код выглядит так:

print(
    (lambda i:(
        "Correct"
        if ((type(lambda:None))(i, {}))\
           (i, ord, raw_input("Flag: "))
        else "Incorrect"
    ))
    (__import__('marshal').loads(<some_other_string>))
)

Обратим внимание на использование функции raw_input - программа написана для Python 2.
Рассмотрим, что происходит внутри lambda-функции. type(lambda:None) это ничто иное как types.FunctionType, конструктор которого принимает в качестве аргументов параметры code и globals; в качестве code передается аргумент lambda-функции, а словарь globals пуст. Далее эта функция вызывается с тремя аргументами: i (тот самый code object), ord (встроенная функция) и, собственно, флаг.

Попробуем исследовать code object.

>>> c = (__import__('marshal').loads(<some_other_string>)
>>> import dis
>>> dis.dis(c) # дизассемблируем
Traceback (most recent call last):
  File "<strin>", line 1, in <module>
  File "/usr/lib/python2.7/dis.py", line 43, in dis
    disassemble(x)
  File "/usr/lib/python2.7/dis.py", line 64, in disassemble
    labels = findlabels(code)
  File "/usr/lib/python2.7/dis.py", line 166, in findlabels
    oparg = ord(code[i]) + ord(code[i+1])*256
IndexError: string index out of range
>>>

Упс, кажется, у нас некорректный байткод. Попробуем добавить несколько лишних байт, чтобы обойти IndexError:

>>> dis.dis(c.co_code + b'\0\0')
          0 LOAD_FAST           2 (2)
          3 GET_ITER       
          4 LOAD_FAST           0 (0)
          7 LOAD_ATTR           0 (0)
         10 LOAD_CONST          0 (0)
         13 SLICE+1        
         14 GET_ITER       
         15 LOAD_FAST           1 (1)
         18 DUP_TOP        
         19 ROT_THREE      
         20 ROT_THREE      
    >>   21 FOR_ITER           52 (to 76)
         24 ROT_THREE      
         25 ROT_THREE      
         26 ROT_TWO        
         27 CALL_FUNCTION       1
         30 DUP_TOP        
         31 LOAD_CONST          1 (1)
         34 DUP_TOP        
         35 ROT_THREE      
         36 BINARY_LSHIFT  
         37 ROT_THREE      
         38 BINARY_RSHIFT  
         39 BINARY_OR      
         40 LOAD_CONST          2 (2)
         43 BINARY_AND     
         44 ROT_FOUR       
         45 ROT_FOUR       
         46 DUP_TOP        
         47 ROT_THREE      
         48 ROT_THREE      
         49 FOR_ITER           32 (to 84)
         52 ROT_THREE      
         53 ROT_TWO        
         54 ROT_THREE      
         55 ROT_THREE      
         56 CALL_FUNCTION       1
         59 ROT_FOUR       
         60 ROT_FOUR       
         61 ROT_FOUR       
         62 COMPARE_OP          2 (==)
         65 POP_JUMP_IF_FALSE    85
         68 ROT_TWO        
         69 DUP_TOP        
         70 ROT_FOUR       
         71 ROT_FOUR       
         72 ROT_FOUR       
         73 JUMP_ABSOLUTE      21
    >>   76 POP_TOP        
         77 POP_TOP        
         78 FOR_ITER           11 (to 92)
         81 JUMP_FORWARD        2 (to 86)
    >>   84 POP_TOP        
    >>   85 POP_TOP        
    >>   86 POP_TOP        
         87 POP_TOP        
         88 LOAD_CONST          3 (3)
         91 RETURN_VALUE   
    >>   92 LOAD_CONST          4 (4)
         95 RETURN_VALUE   
         96 <196>           50356
         99 DELETE_SLICE+2 
        100 <69>           
        101 LOAD_CONST      18103 (18103)
        104 BINARY_POWER   
        105 INPLACE_ADD    
        106 <245>           21398
        109 <245>             998
        112 POP_JUMP_IF_TRUE 17397
        115 <245>           17159
        118 <230>           13846
        121 DELETE_SLICE+1 
        122 BINARY_MODULO  
        123 <215>               0
>>>

Теперь осталось разобраться в алгоритме.
[флаг хранится внутри самого байткода, начиная с позиции 96. Чтобы не strings'илось, каждый символ закодирован как chr(((ord(i)<<4)|(ord(i)>>4))&255).]

Флаг: LKLCTF{d1s_i5_n07_4_p4nac3a}
