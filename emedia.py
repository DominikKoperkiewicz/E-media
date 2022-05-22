# load and show an image with Pillow
from PIL import Image, ExifTags
import numpy
import base64
import os

# Open the image form working directory
filename = 'Lenna.png'

image = Image.open(filename)
fbyte = open(filename, "rb")

tmp = fbyte.read(8).hex()

signature = "89504e470d0a1a0a"
if tmp == signature:
    print("FORMAT: [PNG]")
else:   
    print("This file is not PNG!")
    quit()

end = False

# ****************** DEFINITIONS ******************

def read_chunk():
    tmp = fbyte.read(4).hex()
    if tmp =='':
        quit()

    length = int(tmp,16)
    chunk_type = fbyte.read(4).decode()
    if chunk_type == '':
        quit()
    print('\n', chunk_type, '| CHUNK LENGTH:', length, 'bytes')

    match chunk_type:
        case 'IHDR':
            IHDR(length)
        case 'sRGB':
            sRGB(length)
        case 'PLTE':
            PLTE(length)
        case 'IEND':
            IEND()
        case _:
            print('\tUNKNOW CHUNK')
            fbyte.read(length)

    crc = fbyte.read(4).hex()
    print('\nCRC:', crc)
    print('_________________________________')

def IHDR(len):
    if len != 13:
        print('Invalid IHDR length')
        quit()
    width = int(fbyte.read(4).hex(),16)
    height = int(fbyte.read(4).hex(),16)
    depth = int(fbyte.read(1).hex(),16)
    colortype = int(fbyte.read(1).hex(),16)
    comp = int(fbyte.read(1).hex(),16)
    filt = int(fbyte.read(1).hex(),16)
    inte = int(fbyte.read(1).hex(),16)
    print('\tWidth:', width)
    print('\tHeight:', height)
    print('\tBit depth:', depth)
    print('\tColor Type:', color_type(colortype))
    print('\tCompression method:', compression_method(comp))
    print('\tFilter method:', filter_method(filt))
    print('\tInterlace method:', interlace_method(inte))

# ********** IHDR FUNCTIONS **********
def color_type(ct):
    match ct:
        case 0:
            return 'Grayscale'
        case 2:
            return 'RGB'
        case 3:
            return 'Palette'
        case 4:
            return 'Grayscale with alpha'
        case 6:
            return 'RGB with alpha' 
        case _:
            print('Invalid color type')
            quit()

def compression_method(cm):
    if cm == 0:
        return 'Deflate/Inflate'
    else:
        print('Invalid compression method')
        quit()

def filter_method(fm):
    match fm:
        case 0:
            return 'None'
        case 1:
            return 'Sub'
        case 2:
            return 'Up'
        case 3:
            return 'Average'
        case 4:
            return 'Paeth'
        case _:
            print('Invalid filter method')
            quit()

def interlace_method(im):
    match im:
        case 0:
            return 'No interlace'
        case 1:
            return 'Adam7'
        case _:
            print('Invalid interlace method')
            quit()
# ************************************

def sRGB(len):
    if len != 1:
        print('Invalid IHDR length')
        quit()
    rend = int(fbyte.read(1).hex(),16)
    print('\tRendering intent:', rendering_intent(rend))

def rendering_intent(ri):
    match ri:
        case 0: 
            return 'Perceptual'
        case 1: 
            return 'Relative colorimetric'
        case 2: 
            return 'Saturation'
        case 3: 
            return 'Absolute colorimetric'
        case _:
            print('Invalid rendering intent value')
            quit()

plt = None
def PLTE(len):
    if len % 3 != 0:
        print("Invalid chunk length")
        exit()
    for i in range(0, len % 3):
        plt[i] = [int(fbyte.read(1).hex(),16), int(fbyte.read(1).hex(),16), int(fbyte.read(1).hex(),16)]
    Image.fromarray(plt).save("palette.png")
    img = Image.open("palette.png")
    img.show()


def IEND():
    print('End of the file')
    global end 
    end = True

def anonymization():
    if os.path.exists("anonymous.png"):
        os.remove("anonymous.png")    
    f = open("anonymous.png", "xb")
    global fbyte
    fbyte = open(filename, "rb")
    global end
    end = False

    sign = fbyte.read(8)
    f.write(sign)

    while not end:
        chunk_size = fbyte.read(4)
        chunk_type = fbyte.read(4)
        decoded = chunk_type.decode()
        if decoded == 'IHDR' or decoded == 'IDAT' or decoded == 'PLTE':
            f.write(chunk_size)                             # CHUNK SIZE
            f.write(chunk_type)                             # CHUNK TYPE
            f.write(fbyte.read(int(chunk_size.hex(),16)))   # CHUNK CONTENT
            f.write(fbyte.read(4))                          # CRC
        elif decoded == 'IEND':
            f.write(chunk_size)                             # CHUNK SIZE
            f.write(chunk_type)                             # CHUNK TYPE
            f.write(fbyte.read(int(chunk_size.hex(),16)))   # CHUNK CONTENT
            f.write(fbyte.read(4))                          # CRC
            print('anonymization finished!')
            return
        else:
            fbyte.read(int(chunk_size.hex(),16)+4)
    
    length = int(tmp,16)
    chunk_type = fbyte.read(4).decode()


def anonymization_2(A):
    im = Image.fromarray(A)
    im.save("anonymous2.png")

while not end:
    read_chunk()

fbyte.close()

#print('Anonymize the image (y/n)')
#if input() == 'y':
anonymization()
arr = numpy.array(image)
anonymization_2(arr)

quit()

#arr = numpy.array(image)

# summarize some details about the image
# print(image.format)
# print(image.size)
# print(image.mode)

# show the image
#image.show()