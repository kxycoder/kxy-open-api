#!/usr/bin/python
# -*- coding:utf-8 -*-

import binascii,sys
print(sys.path)
from pyDes import des, CBC, PAD_PKCS5

# key和iv可放置于config中
class Crypto:
    def __init__(self):
        self.key = 'f87e43f9'

    def encrypt(self, password):
        iv = self.key
        k = des(self.key, CBC, iv, pad=None, padmode=PAD_PKCS5)
        en = k.encrypt(password, padmode=PAD_PKCS5)
        return binascii.b2a_hex(en).decode('utf-8')

    def decrypt(self,text) :
        iv = self.key
        k = des(self.key, CBC, iv, pad=None, padmode=PAD_PKCS5)
        de = k.decrypt(binascii.a2b_hex(text), padmode=PAD_PKCS5)
        return de.decode('utf-8')