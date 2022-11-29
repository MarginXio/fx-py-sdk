# -*- coding: utf-8 -*-
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Sign_Cipher_pkcs1_v1_5
from Crypto.Hash import SHA


def encrypt_data(encrypt_message:bytes, rsa_public_key)->bytes:
    """RSA分段加密"""
    def _encrypt_data(encrypt_params, rsa_public_key):
        rsakey = RSA.importKey(base64.b64decode(rsa_public_key))
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        return cipher.encrypt(encrypt_params)
    if type(encrypt_message) is not bytes:
        params = bytes(encrypt_message, "utf-8")
    else:
        params = encrypt_message
    one_len = 100
    ret_data = b''
    for i in range(0, len(params), one_len):
        ret_data += _encrypt_data(params[i:i + one_len], rsa_public_key)
    return ret_data


def decrypt_data(encrypted_message:bytes, rsa_private_key:str)->bytes:
    """RSA分段解密"""
    if type(encrypted_message) is not bytes:
        encrypted_message = base64.b64decode(encrypted_message)
        # encrypted_message = bytes(encrypted_message, encoding='utf-8')
    private_key_object = RSA.importKey(rsa_private_key)
    cipher = Cipher_pkcs1_v1_5.new(private_key_object)
    # 1024 bit的证书用128，2048 bit证书用256位
    one_len = 128
    ret_data = b''
    for i in range(0, len(encrypted_message), one_len):
        ret_data += cipher.decrypt(encrypted_message[i:i + one_len], None)
    return ret_data
    # return cipher.decrypt(encrypted_message, None).decode("utf-8")


def rsa_sign(encrypted_message:bytes, rsa_private_key:str)->bytes:
    """RSA私钥签名"""
    if type(encrypted_message) is not bytes:
        encrypted_message = bytes(encrypted_message, encoding='utf-8')
    private_key_object = RSA.importKey(rsa_private_key)
    signer = Sign_Cipher_pkcs1_v1_5.new(private_key_object)
    digest = SHA.new()
    digest.update(encrypted_message)
    return signer.sign(digest)
    # return base64.b64encode(signature).decode("utf-8")


def rsa_verify_sign(encrypted_message:bytes, sign:bytes, rsa_public_key:str)->bool:
    """RSA公钥验签"""
    if type(encrypted_message) is not bytes:
        encrypted_message = bytes(encrypted_message, "utf-8")
    if type(sign) is not bytes:
        sign = bytes(sign, "utf-8")
    public_key_object = RSA.importKey(rsa_public_key)
    verifier = Sign_Cipher_pkcs1_v1_5.new(public_key_object)
    digest = SHA.new()
    digest.update(encrypted_message)
    return verifier.verify(digest, sign)
    # return verifier.verify(SHA.new(encrypted_message), base64.b64decode(sign))


def bytes_to_str(bytes_obj:bytes)->str:
    """bytes转str"""
    if type(bytes_obj) is not str:
        str_obj = bytes_obj.decode("utf-8")
    else:
        str_obj = bytes_obj
    return str_obj


def str_to_bytes(str_obj:str)->bytes:
    """str装bytes"""
    if type(str_obj) is not bytes:
        bytes_obj = bytes(str_obj, encoding="utf-8")
    else:
        bytes_obj = str_obj
    return bytes_obj


def base64_encode(text:bytes)->bytes:
    """base64编码"""
    if type(text) is not bytes:
        text = text.encode('utf-8')
    return base64.b64encode(text)


def base64_decode(encoded_text:bytes)->str:
    """base64转码"""
    if type(encoded_text) is not bytes:
        encoded_text = encoded_text.encode('utf-8')
    return base64.b64decode(encoded_text)
