#!/usr/bin/python3

import os
from Crypto.Hash import SHA256
from Crypto.Cipher import AES

#https://www.dlitz.net/software/pycrypto/api/2.6/Crypto.Cipher.AES-module.html

def crypto_AES_CBC_Encrypt(input, key):
    input = input + b"\0" * (AES.block_size - len(input) % AES.block_size)
    iv = os.urandom(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    output = iv + cipher.encrypt(input)
    return output

def crypto_AES_CBC_Decrypt(input, key):
    iv = input[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(input[AES.block_size:])
    output = plaintext.rstrip(b"\0")
    return output


def crypto_AES_ECB_Encrypt(input, key):
    input = input + b"\0" * (AES.block_size - len(input) % AES.block_size)
    iv = os.urandom(AES.block_size)
    cipher = AES.new(key, AES.MODE_ECB, iv)
    output = iv + cipher.encrypt(input)
    return output

def crypto_AES_ECB_Decrypt(input, key):
    iv = input[:AES.block_size]
    cipher = AES.new(key, AES.MODE_ECB, iv)
    plaintext = cipher.decrypt(input[AES.block_size:])
    output = plaintext.rstrip(b"\0")
    return output


if __name__ == '__main__':
    key = os.urandom(32)
    message = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'

    cryptoEncrypt(message, key)
