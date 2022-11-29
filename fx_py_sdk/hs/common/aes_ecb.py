# -*- coding: utf-8 -*-
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = 16  # Bytes


class AESCipher:
    def __init__(self, key:str):
        if type(key) is not bytes:
            self.key = base64.b64decode(key)  # 16位
        else:
            self.key = key

    def encrypt(self, raw:bytes)->bytes:
        if type(raw) is not bytes:
            raw = bytes(raw, "utf-8")
        cipher = AES.new(self.key, AES.MODE_ECB)
        return cipher.encrypt(pad(raw, BLOCK_SIZE))

    def decrypt(self, enc:bytes)->bytes:
        if type(enc) is not bytes:
            enc = bytes(enc, "utf-8")
        cipher = AES.new(self.key, AES.MODE_ECB)
        return unpad(cipher.decrypt(enc), BLOCK_SIZE)
