from abc import ABC, abstractmethod
from Crypto.Cipher import AES

class TextCrypto:
    @abstractmethod
    def Encrypt(self, message): pass
    @abstractmethod
    def Decrypt(self, message): pass

class PlainTextCrypto(TextCrypto):
    def Encrypt(self, message):
        return bytes(message, "utf-8")
    def Decrypt(self, message):
        return message.decode("utf-8")

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[0:-ord(s[-1])]

class Aes128TextEncryptor(TextCrypto):
    def __init__(self, encryption_key):
        self.aes = AES.new(encryption_key, AES.MODE_ECB)
    def Encrypt(self, message):
        message = pad(message)
        message = bytes(message, "utf-8")
        return self.aes.encrypt(message)
    def Decrypt(self, message):
        ret = self.aes.decrypt(message)
        ret = ret.decode("utf-8")
        return unpad(ret)