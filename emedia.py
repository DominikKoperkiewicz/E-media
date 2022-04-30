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


while True:
    read_chunk()


# summarize some details about the image
# print(image.format)
# print(image.size)
# print(image.mode)

# arr = numpy.array(image)

# print(arr[0][0])

# show the image
#image.show()