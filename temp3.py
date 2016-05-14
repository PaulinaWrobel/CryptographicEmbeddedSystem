#!/usr/bin/python3

from PIL import Image
import numpy as np
from Crypto.Cipher import AES
from Crypto import Random

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

im = Image.open('out.jpg')

# In this case, it's a 3-band (red, green, blue) image
# so we'll unpack the bands into 3 separate 2D arrays.
r, g, b = np.array(im).T

# Let's make an alpha (transparency) band based on where blue is < 100
a = np.zeros_like(b)
a[b < 100] = 255

# Random math... This isn't meant to look good...
# Keep in mind that these are unsigned 8-bit integers, and will overflow.
# You may want to convert to floats for some calculations.
#r = (b + g) * 5
key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'


enc = encrypt(r, key)




# Put things back together and save the result...
im = Image.fromarray(np.dstack([item.T for item in (enc,g,b,a)]))

im.save('output.jpg')

print(type(r))
