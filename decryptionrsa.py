from cmath import e
from fileinput import filename
from this import d
import numpy
import sympy
import rsa
import os

def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key)
    except:
        return False

path = 'encryptedrsa.png'
path_en = 'decryptedrsa.png'

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
d = 4065916269448447564634580615933761174370013091130374302263136822075599671109726157260559855536812302533254669223713903531715071205986330847444913901892593
n = 22062981595264846710096059146196071286240213043136373733321895441456800353065856154886964770980922978001039546853511351554684249909980532939577382964800479
p = 162613953912208321411479180185254428191979221919933196078939209612522834425471
q = 135677050243647372948848778974435927667671339244926662422552757961515294284449

(pubkey, privkey) = rsa.newkeys(512)

pubkey.e = e
pubkey.n = n

privkey.e = e
privkey.d = d
privkey.n = n
privkey.p = p
privkey.q = q
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
        for i in range(0, length // 65):
            bytes = fbyte.read(65)
            #cyp = int.from_bytes(bytes, 'big')
            data = rsa.decrypt(bytes, privkey)
            #decr.write(data.to_bytes(63, byteorder ='big'))
            decr.write(data)
        decr.write(fbyte.read(4))



while True:
    handle_chunk()