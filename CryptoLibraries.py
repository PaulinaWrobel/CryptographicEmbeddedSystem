#!/usr/bin/python3

import os
from Crypto.Hash import SHA256
from Crypto.Cipher import AES

#https://www.dlitz.net/software/pycrypto/api/2.6/Crypto.Cipher.AES-module.html

def cryptoEncrypt(input, key):
    #print("Length before: %s" % len(input))
    input = input + b"\0" * (AES.block_size - len(input) % AES.block_size)
    #print("Length after: %s" % len(input))
    iv = os.urandom(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    output = iv + cipher.encrypt(input)
    return output

def cryptoDecrypt(input, key):
    iv = input[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(input[AES.block_size:])
    output = plaintext.rstrip(b"\0")
    return output



if __name__ == '__main__':
    key = os.urandom(32)
    message = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'

    cryptoEncrypt(message, key)
