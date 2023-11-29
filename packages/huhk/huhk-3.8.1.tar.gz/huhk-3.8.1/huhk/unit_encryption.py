"""
    加解密
"""

import binascii
from pyDes import des, CBC, PAD_PKCS5
import base64
from Crypto.Cipher import PKCS1_v1_5, AES
from Crypto import Random
from Crypto.PublicKey import RSA


def des_encryption(value, KEY=b'huhk0001'):
    """
    字符串，des加密
    :param value: str
    :param KEY: str 非必填
    :return: str
    """
    des_obj = des(KEY, CBC, KEY, pad=None, padmode=PAD_PKCS5)
    secret_bytes = des_obj.encrypt(value.encode(), padmode=PAD_PKCS5)
    return str(binascii.b2a_hex(secret_bytes), encoding="utf8")


def des_decryption(value, KEY=b'huhk0001'):
    """
    字符串，des解密
    :param value: str
    :param KEY: 非必填，需和加密key一致
    :return: str
    """
    des_obj = des(KEY, CBC, KEY, pad=None, padmode=PAD_PKCS5)
    secret_bytes = binascii.a2b_hex(bytes(value, encoding="utf8"))
    return str(des_obj.decrypt(secret_bytes, padmode=PAD_PKCS5), encoding="utf8")


# ------------------------生成密钥对------------------------
def create_rsa_pair(is_save=False):
    '''
    创建rsa公钥私钥对
    :param is_save: default:False
    :return: public_key, private_key
    '''
    f = RSA.generate(2048)
    private_key = f.exportKey("PEM")  # 生成私钥
    public_key = f.publickey().exportKey()  # 生成公钥
    if is_save:
        with open("crypto_private_key.pem", "wb") as f:
            f.write(private_key)
        with open("crypto_public_key.pem", "wb") as f:
            f.write(public_key)
    return public_key, private_key


def read_public_key(file_path="crypto_public_key.pem") -> bytes:
    with open(file_path, "rb") as x:
        b = x.read()
        return b


def read_private_key(file_path="crypto_private_key.pem") -> bytes:
    with open(file_path, "rb") as x:
        b = x.read()
        return b


# ------------------------加密------------------------
def rsa_encryption(text: str, public_key: bytes):
    # 字符串指定编码（转为bytes）
    text = text.replace('\r\n', '\n').encode('utf-8')
    key = RSA.importKey(public_key)
    # 构建公钥对象
    cipher_public = PKCS1_v1_5.new(key)
    # 加密（bytes）
    text_encrypted = cipher_public.encrypt(text)
    # base64编码，并转为字符串
    text_encrypted_base64 = base64.b64encode(text_encrypted).decode()
    return text_encrypted_base64


# ------------------------解密------------------------
def rsa_decryption(text_encrypted_base64: str, private_key: bytes):
    # 字符串指定编码（转为bytes）
    text_encrypted_base64 = text_encrypted_base64.encode('utf-8')
    # base64解码
    text_encrypted = base64.b64decode(text_encrypted_base64)
    # 构建私钥对象
    cipher_private = PKCS1_v1_5.new(RSA.importKey(private_key))
    # 解密（bytes）
    text_decrypted = cipher_private.decrypt(text_encrypted, Random.new().read)
    # 解码为字符串
    text_decrypted = text_decrypted.decode()
    return text_decrypted


def aesEncrypt(key, data):
    '''
    AES的ECB模式加密方法
    :param key: **
    :param data:被加密字符串（明文）
    :return:密文
    '''
    key = key.encode('utf8')
    pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
    # 字符串补位
    data = pad(data)
    cipher = AES.new(key, AES.MODE_ECB)
    # 加密后得到的是bytes类型的数据，使用Base64进行编码,返回byte字符串
    result = cipher.encrypt(data.encode())
    encodestrs = base64.b64encode(result)
    enctext = encodestrs.decode('utf8')
    # print(enctext)
    return enctext


def aesDecrypt(key, data):
    '''
    :param key: **
    :param data: 加密后的数据（密文）
    :return:明文
    '''
    key = key.encode('utf8')
    data = base64.b64decode(data)
    cipher = AES.new(key, AES.MODE_ECB)

    unpad = lambda s: s[:-ord(s[len(s) - 1:])]
    # 去补位
    text_decrypted = unpad(cipher.decrypt(data))
    text_decrypted = text_decrypted.decode('utf8')
    # print(text_decrypted)
    return text_decrypted


if __name__ == '__main__':
    # 生成密钥对
    # create_rsa_pair(is_save=True)
    # public_key = read_public_key()
    # private_key = read_private_key()
    # public_key, private_key = create_rsa_pair(is_save=False)

    # 加密
    text = 'Pickup@123456'
    key = '1111111111111111'
    aa = aesEncrypt(key, text)
    print(aesDecrypt(key, aa))
