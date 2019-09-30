#!/usr/bin/python3
#coding=utf-8
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto import Random
from Crypto.Util.py3compat import *
from Crypto.Util.Padding import pad, unpad

import base64
import sys
import hashlib

BS = AES.block_size

class AES_UTIL:
    @staticmethod
    def encrypt(plaintext, key):
        iv = Random.new().read(BS)
        print(iv)
        padded_key = pad(key.encode(),16)

        encrypter = AES.new(padded_key, AES.MODE_CBC, iv)

        padded_plaintext = pad(plaintext, 16)

        hashed_key = hashlib.sha256(padded_key).digest()
        hashed_plaintext = hashlib.sha256(padded_plaintext).digest()
        print(len(hashed_plaintext))

        encrypted_text = encrypter.encrypt(padded_plaintext)
         
        return hashed_key + hashed_plaintext + iv + encrypted_text

    @staticmethod
    def decrypt(enc, key):
        hashed_key = enc[:32]
        padded_key = pad(key.encode(),16)
        if(hashed_key != hashlib.sha256(padded_key).digest()) :
            print("key err0r")
            exit(1)
        hashed_text = enc[32:64]

        iv = enc[64:(64 + BS)]
        print(iv)
        cipher = AES.new(padded_key, AES.MODE_CBC, iv)

        enc = cipher.decrypt(enc[64+BS:])
        plaintext = unpad(enc, 16)
        
        padded_plaintext = pad(plaintext, 16)
        if(hashed_text != hashlib.sha256(padded_plaintext).digest()) :
            print("text err0r")
            exit(1)
        

        return plaintext

    @staticmethod
    def operate(commands):

        # arguments judged
        if len(commands) == 4 and (commands[1] == '-d' or commands[1] == '-e'):
            command = commands[1]
            input_file = commands[2]
            output_file = commands[3]
        else:
            print('Syntax:')
            print('To encrypt:  ./duke-crypter -e <input_file> <output_file>')
            print('To decrypt:  ./duke-crypter -d <input_file> <output_file>')
            exit(1)

        try:
            # support large file
            with open(input_file, 'rb') as infile:
                data = infile.read()
        except IOError:
            print('Err: can\'t not find ', input_file)
            exit(1)
        
        key= input('please input your key:\n')

        # enc data with key
        if command == '-e':
            enc_data = AES_UTIL.encrypt(data,key)
        # dec data delete key
        elif command == '-d':
            try:
                dec_data = AES_UTIL.decrypt(data,key)
            except Exception as e:
                print(str(e))
                print('Err: wrong key or file has been changed!')
                exit(1)

        # write cover space file
        try:
            if command == '-e':
                with open(output_file, 'wb') as ofile:
                    ofile.write(enc_data)
            elif command == '-d':
                # recover into true file
                with open(output_file, 'wb') as ofile:
                    ofile.write(dec_data)
        except IOError:
            print('Exp: io exception!')
            exit(1)
        else:
            print('operate success!')


if __name__ == '__main__':

    commands = sys.argv
    AES_UTIL.operate(commands)
    exit(0)