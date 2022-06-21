from cmath import e
from fileinput import filename
from this import d
import numpy
import sympy
import rsa
import os

path = 'encrypted.png'
path_en = 'decrypted.png'

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
d = 2491649152858139171598007686466269406783187795249485930866680452602344327054342668957770918414990599052638620371255990723975388138265999781482855032633425  
n = 18997154246968395567706157295419827485272290212353782777345896426545700568661544863928552273259276050575298307062339812195108135203782536666161697962651279 
p = 140995536840657577233407133269019158842328087597264065956965901902128084125233
q = 134735855280564896048024576202501348396831381075906909213935013442959860355263
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
            cyp = int.from_bytes(bytes, 'big')
            data = pow(cyp, d, n)
            decr.write(data.to_bytes(63, byteorder ='big'))
            
        decr.write(fbyte.read(4))



while True:
    handle_chunk()