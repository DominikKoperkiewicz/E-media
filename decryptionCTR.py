from cmath import e
from fileinput import filename
from this import d
import numpy
import sympy
import rsa
import os

path = 'encryptedCTR.png'
path_en = 'decryptedCTR.png'

fbyte = open(path, "rb")
decr = open(path_en, "wb")

tmp = fbyte.read(8)

signature = "89504e470d0a1a0a"
if tmp.hex() == signature:
    print("FORMAT: [PNG]")
    decr.write(tmp)
else:   
    print("This file is not PNG!")
    quit()

# KLUCZ
e = 35537
d = 2843737444643462363766615098410423393428528634261196125116840433709719730369132680433332064042858652383305479796334874729887914425727964519083397260871729  
n = 33957626871738817883459072833404306496058340751256763003453346267722550422758395547188987986537393954575350602835959619139804473905985799422389879714152921 
p = 223276270619364782079311060510894904220861542182422897491471566680728219751877
q = 152087934725624480090204756262142232023554883903363190250149389759323382976773
# *****
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
        decr.write(tmp)
        decr.write(chunk_type)
        content = fbyte.read(length+4)
        decr.write(content)
    else:
        decr.write(tmp)
        decr.write(chunk_type)
        ctr = 0
        for i in range(0, length // 65):
            ctr += 1
            bytes = fbyte.read(65)
            cyp = int.from_bytes(bytes, 'big')
            data = pow(cyp, d, n) ^ ctr
            decr.write(data.to_bytes(63, byteorder ='big'))
            
        decr.write(fbyte.read(4))



while True:
    handle_chunk()