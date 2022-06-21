from cmath import e
from fileinput import filename
from this import d
import numpy
import sympy
import rsa
import os

def encrypt(message, key):
    return rsa.encrypt(message, key)

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
	# make a the bigger one and b the lesser one
	swapped = False
	if a < b:
		a, b = b, a
		swapped = True
	# ca and cb store current a and b in form of
	# coefficients with initial a and b
	# a' = ca[0] * a + ca[1] * b
	# b' = cb[0] * a + cb[1] * b
	ca = (1, 0)
	cb = (0, 1)
	while b != 0:
		# k denotes how many times number b
		# can be substracted from a
		k = a // b
		# a  <- b
		# b  <- a - b * k
		# ca <- cb
		# cb <- (ca[0] - k * cb[0], ca[1] - k * cb[1])
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
path_en = 'encryptedrsa.png'

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

#e, d, n, p, q = keygen()
e = 35537
d = 15272211762309562652006451362125678963931760127202306313145293065206284497700600957269923718730231084992317221308918607098836429781159186823517743292713473 
n = 24753869527808206520609042739149840517274479345057621867742042401743933053354306329584289003682745620187136496611981214030739277182479127447668869266955247 
p = 148704679384188243326923446541544312216591127637222686736974795563349441067801
q = 166463285690257057835022060003066614243959711706378092866256545042804049688647
# e = 35537
# d = 28888329163554910079672951725607980111420299596801092523374578157934321699120435024048879255987046602806930627460668276741614198279021571812154579548214513
# n = 29555334777177222959589396443729114415417969966072273643390309025435784949522235589202111547476976208900496714499884035818449706512512981722898700550016853
# p = 164794537517939759559241125384260209422641871038674835101011299220595223324357
# q = 179346568292409502023988821610404252466041980612593092653381176851063627976529
(pubkey, privkey) = rsa.newkeys(1024)

pubkey.e = e
pubkey.n = n

privkey.e = e
privkey.d = d
privkey.n = n
privkey.p = p
privkey.q = q

print("d =", d)
print("n =", n)

def handle_chunk():
    tmp = fbyte.read(4)
    if tmp.hex() =='':
        quit()

    length = int(tmp.hex(),16)
    print(length)
    chunk_type = fbyte.read(4)
    if chunk_type.decode() == '':
        quit()
    if chunk_type.decode() != 'IDAT':
        encr.write(tmp)
        encr.write(chunk_type)
        content = fbyte.read(length+4)
        encr.write(content)
    else:
        block_number = int(length/53)
        blocks = []
        for i in range(0, block_number):
            bytes = fbyte.read(53)
            #num = int.from_bytes(bytes, 'big')
            #cyp = pow(num, e, n)
            cyp = encrypt(bytes, pubkey)
            blocks.append(cyp)
        rest = length - block_number * 53
        if rest > 0:
            bytes = fbyte.read(rest)
            #num = int.from_bytes(bytes, 'big')
            #cyp = pow(num, e, n)
            cyp = encrypt(bytes, pubkey)
            blocks.append(cyp)
        encr.write(((block_number+1)*55).to_bytes(4, byteorder ='big'))
        encr.write(chunk_type)
        for block in blocks:
            #encr.write(block.to_bytes(65, byteorder ='big'))
            encr.write(block)
        encr.write(fbyte.read(4))
        

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

