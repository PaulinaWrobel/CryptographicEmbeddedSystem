#!/usr/bin/python3

from Crypto import Random
from Crypto.Cipher import AES
import os
import datetime
import time

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    message = pad(message)
    iv = os.urandom(AES.block_size)
    #iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

def encrypt_file(file_name, file_name_out, key):
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key)
    with open(file_name_out, 'wb') as fo:
        fo.write(enc)

def decrypt_file(file_name, file_name_out, key):
    with open(file_name, 'rb') as fo:
        ciphertext = fo.read()
    dec = decrypt(ciphertext, key)
    with open(file_name_out, 'wb') as fo:
        fo.write(dec)


if __name__ == '__main__':

    #key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'
    key = os.urandom(32)
    encrypt_file('original.txt', "out123.txt", key)
    decrypt_file("out123.txt", 'original.txt.enc', key)
    print("urandom: %s" % key)
    a = datetime.datetime.now()
    aa = time.time()
    time.sleep(5.8)
    b = datetime.datetime.now()
    bb = time.time()
    print("b-a: %s" % (b-a).total_seconds())
    print("bb-aa: %s" % (bb-aa))
