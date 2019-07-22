import dis

globals().update(dis.opmap)

flag = 'LKLCTF{d1s_i5_n07_4_p4nac3a}'
names = ('co_code',)
consts = (96, 4, 255, False, True)

bc = ''.join(map(chr, (
    LOAD_FAST, 2, 0, # u
    GET_ITER, # it_u
    LOAD_FAST, 0, 0, # it_u codeobj
    LOAD_ATTR, 0, 0, # it_u bc
    LOAD_CONST, 0, 0, # it_u bc lbc
    dis.opmap['SLICE+1'], # it_u k
    GET_ITER, # it_u it_k
    LOAD_FAST, 1, 0, # it_u it_k ord
    DUP_TOP, # it_u it_k ord ord
    ROT_THREE, ROT_THREE, # it_u ord ord it_k
# :loop
    FOR_ITER, 52, 0, # it_u ord ord it_k b_k; branch to :key_end
    ROT_THREE, ROT_THREE, # it_u ord it_k b_k ord
    ROT_TWO, # it_u ord it_k ord b_k
    CALL_FUNCTION, 1, 0, # it_u ord it_k c_k
    DUP_TOP, # it_u ord it_k c_k c_k
    LOAD_CONST, 1, 0, # it_u ord it_k c_k c_k 4
    DUP_TOP, # it_u ord it_k c_k c_k 4 4
    ROT_THREE, # it_u ord it_k c_k 4 c_k 4
    BINARY_LSHIFT, # it_u ord it_k c_k 4 (c_k<<4)
    ROT_THREE, # it_u ord it_k (c_k<<4) c_k 4
    BINARY_RSHIFT, # it_u ord it_k (c_k<<4) (c_k>>4) 
    BINARY_OR, # it_u ord it_k sh
    LOAD_CONST, 2, 0, # it_u ord it_k sh 255
    BINARY_AND, # it_u ord it_k i_k
    ROT_FOUR, ROT_FOUR, # it_k i_k it_u ord
    DUP_TOP, # it_k i_k it_u ord ord
    ROT_THREE, ROT_THREE, # it_k i_k ord ord it_u
    FOR_ITER, 32, 0, # it_k i_k ord ord it_u c_u; branch to :fail4
    ROT_THREE, # it_k i_k ord c_u ord it_u
    ROT_TWO, # it_k i_k ord c_u it_u ord
    ROT_THREE, ROT_THREE, # it_k i_k ord it_u ord c_u
    CALL_FUNCTION, 1, 0, # it_k i_k ord it_u i_u
    ROT_FOUR, ROT_FOUR, ROT_FOUR, # it_k ord it_u i_u i_k
    COMPARE_OP, 2, 0, # it_k ord it_u (i_u == i_k)
    POP_JUMP_IF_FALSE, 85, 0, # it_k ord it_u; branch to :fail3
    ROT_TWO, # it_k it_u ord
    DUP_TOP, # it_k it_u ord ord
    ROT_FOUR, ROT_FOUR, ROT_FOUR, # it_u ord ord it_k
    JUMP_ABSOLUTE, 21, 0, # branch to :loop
# :key_end # it_u ord ord
    POP_TOP, POP_TOP, # it_u
    FOR_ITER, 11, 0, # branch to :success
    JUMP_FORWARD, 2, 0, # branch to :fail2
# :fail4
    POP_TOP,
# :fail3
    POP_TOP,
# :fail2
    POP_TOP, POP_TOP,
    LOAD_CONST, 3, 0,
    RETURN_VALUE,
# :success
    LOAD_CONST, 4, 0,
    RETURN_VALUE
)))+b''.join(map(chr, (((i<<4)|(i>>4))&255 for i in map(ord, flag))))

import marshal

code = type((lambda:None).func_code)(3, 3, 16, 0, bc, consts, names, ('$', '$$', '$$$'), '<no_source_for_you>', 'check_flag', 0, b'\1\1'*100)
func = type(lambda:None)(code, {})

#import dis
#dis.dis(func) #crashes, so not running

code1 = 'print(lambda i:("Correct"if type(lambda:None)(i,{})(i,ord,raw_input("Flag: "))else "Incorrect"))(__import__(\'marshal\').loads('+repr(marshal.dumps(code))+'))'

import base64

code2 = 'exec(__import__(\'base64\').b64decode("'+''.join(base64.b64encode(code1).split())+'"))'
print code2
