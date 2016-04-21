#!/usr/bin/python3

from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import getpass

class ED(object):
  def getfromuser(self,choice):
    if choice=='key':
        #key=getpass.getpass('Enter AES Key (minimum 16 characters): ')
        key = "12345678qwerytui"
        if len(key)<16:
            print('Key entered too short. Please try again.')
            self.getfromuser(choice)
        #key=key+str(8-len(key)%8)*(8-len(key)%8)
        #print(key)
        return key
    if choice=='IV':
        #IV_seed=input('Enter a seed for the IV: ')
        #print(IV_seed)
        #IV_seed = IV_seed.encode('utf-8')
        #print(IV_seed)
        #IV_seed = unicode(IV_seed,errors='replace')
        IV=SHA256.new()
        IV.update(b'seedseedseedseed')
        IV.digest()
        return str(IV)[0:16]

  def AESEncrypt(self,key,IV,source,dest):
    f = open(source,"rb")
    fstream = f.read()
    print(fstream)
    f.close()
    #AES_stream=AES.new(key,AES.MODE_CBC,IV)
    AES_stream=AES.new(key,AES.MODE_CFB,IV)
    AES_encrypted=AES_stream.encrypt(fstream)

    with open(dest,"wb") as write_file:
        write_file.write(AES_encrypted)
        #write_file.write(AES_encrypted.decode('utf-8','ignore'))

  def AESDecrypt(self,key,IV,source,dest):
    f=open(source,"rb")
    fstream=f.read()
    f.close()
    AES_stream=AES.new(key,AES.MODE_CFB,IV)
    AES_decrypted=AES_stream.decrypt(fstream)
    with open(dest,"wb") as write_file:
        #write_file.write(AES_decrypted.decode('utf-8','ignore'))
        write_file.write(AES_decrypted)

if __name__ == '__main__':
    obj = ED()
    key = obj.getfromuser('key')
    iv = obj.getfromuser('IV')
    obj.AESEncrypt(key,iv,'out.jpg','dest.jpg')
    obj.AESDecrypt(key,iv,'dest.jpg','decr.jpg')
    #obj.AESEncrypt(key,iv,'original.txt','encrypted.txt')
    #obj.AESDecrypt(key,iv,'encrypted.txt','decrypted.txt')
