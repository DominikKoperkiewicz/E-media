from cmath import e
from fileinput import filename
from this import d
import numpy
import sympy
import rsa
import os

def NWD(a, b):
    while b != 0:
        c = a % b
        a = b
        b = c
    return a

def findE(T):
    i = 8
    while NWD(i, T) != 1:
        i += 1
    return i

def findD(e, T):
    eps = 0.0001
    k = 1
    d = (1+k*T) / e
    while d % 1 > eps:
        k += 1
        d = (1+k*T) / e
    return int(d)

def eucalg(a, b):
	swapped = False
	if a < b:
		a, b = b, a
		swapped = True
	ca = (1, 0)
	cb = (0, 1)
	while b != 0:
		k = a // b
		a, b, ca, cb = b, a-b*k, cb, (ca[0]-k*cb[0], ca[1]-k*cb[1])
	if swapped:
		return (ca[1], ca[0])
	else:
		return ca

def keygen():
    tmp = pow(2, 32*8)
    x = sympy.randprime(tmp, 2*tmp)
    y = sympy.randprime(tmp, 2*tmp)

    N = x*y
    T = (x-1)*(y-1)

    e = 35537
    d = eucalg(e, T)[0]
    if d < 0: d += T
    # e = findE(T)
    # d = findD(e, T) 
    return [e, d, N, x, y]

path = 'Lenna.png'
path_en = 'encryptedCTR.png'

fbyte = open(path, "rb")
encr = open(path_en, "wb")

tmp = fbyte.read(8)

signature = "89504e470d0a1a0a"
if tmp.hex() == signature:
    print("FORMAT: [PNG]")
    encr.write(tmp)
else:   
    print("This file is not PNG!")
    quit()

e, d, n, p, q = keygen()

print("e =", e)
print("d =", d)
print("n =", n)
print("p =", p)
print("q =", q)

def handle_chunk():
    tmp = fbyte.read(4)
    if tmp.hex() =='':
        quit()

    length = int(tmp.hex(),16)
    #print(length)
    chunk_type = fbyte.read(4)
    if chunk_type.decode() == '':
        quit()
    if chunk_type.decode() != 'IDAT':
        encr.write(tmp)
        encr.write(chunk_type)
        content = fbyte.read(length+4)
        encr.write(content)
    else:
        ctr = 0
        SIZ = 0
        block_number = int(length/63)
        blocks = []
        for i in range(0, block_number):
            ctr += 1
            bytes = fbyte.read(63)
            num = int.from_bytes(bytes, 'big')
            cyp = pow(num ^ ctr, e, n)
            blocks.append(cyp)
        rest = length - block_number * 63
        bytes = 0
        if rest > 0:
            bytes = fbyte.read(rest)
            num = int.from_bytes(bytes, 'big')
            cyp = pow(num ^ ctr, e, n)
            blocks.append(cyp)
        encr.write((len(blocks)*65).to_bytes(4, byteorder ='big')) # (block_number+1)*65*16+450
        encr.write(chunk_type)
        for block in blocks:
            encr.write(block.to_bytes(65, byteorder ='big'))
            SIZ += len(block.to_bytes(65, byteorder ='big'))
        encr.write(bytes)
        encr.write(fbyte.read(4))
        print(SIZ)
        print(len(blocks)*65)
        

        # encr.write(tmp)
        # encr.write(chunk_type)
        
        # mes = pow(cyp, d, n)
        # encr.write(cyp.to_bytes(65, byteorder ='big'))
        
        # quit()
        # rest = length - block_number * 63
        # if rest > 0:
        #     # DO ZMIANY
        #     bytes = fbyte.read(rest)
        #     num = int.from_bytes(bytes, 'big')
        #     cyp = pow(num, e, n)
        #     encr.write(cyp.to_bytes(rest, byteorder ='big'))
        # encr.write(fbyte.read(4)) # CRC




while True:
    handle_chunk()





# e, d, n, p, q = keygen()

# bytes = fbyte.read(63)
# num = int.from_bytes(bytes, 'big')
# print(bytes)
# print(num)
# print(num.to_bytes(63, byteorder ='big'))

# cyp = pow(num, e, n)
# mes = pow(cyp, d, n)

# print("DEC:",mes.to_bytes(63, byteorder ='big'))

