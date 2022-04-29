# load and show an image with Pillow
from PIL import Image, ExifTags
import numpy
import base64

# Open the image form working directory
image = Image.open('Lenna.png')
fbyte = open("Lenna.png", "rb")

tmp = fbyte.read(8).hex()

signature = "89504e470d0a1a0a"
if tmp == signature:
    print("FORMAT: [PNG]")
else:   
    print("This file is not PNG!")
    quit()

def read_chunk():
    length = int(fbyte.read(4).hex(),16)
    chunk_type = fbyte.read(4).decode()
    if chunk_type == '':
        quit()
    print('\n', chunk_type, '| LENGTH:', length)

    match chunk_type:
        case 'IHDR':
            IHDR(length)
        case _:
            print('UNKNOW CHUNK')

    crc = fbyte.read(4).hex()
    print('CRC: ', crc)

def IHDR(len):
    print(fbyte.read(len).hex())

read_chunk()
read_chunk()


#while True:
    #read_chunk()

# summarize some details about the image
# print(image.format)
# print(image.size)
# print(image.mode)

# arr = numpy.array(image)

# print(arr[0][0])

# show the image
#image.show()