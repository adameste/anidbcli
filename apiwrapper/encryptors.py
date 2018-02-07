from abc import ABC, abstractmethod
from Crypto.Cipher import AES

class TextCrypto:
    @abstractmethod
    def Encrypt(self, message): pass
    @abstractmethod
    def Decrypt(self, message): pass

class PlainTextCrypto(TextCrypto):
    def Encrypt(self, message):
        return message
    def Decrypt(self, message):
        return message

class Aes128TextEncryptor(TextCrypto):
    def __init__(self, encryption_key):
        self.aes = AES.new(encryption_key, AES.MODE_ECB)
    def Encrypt(self, message):
        return self.aes.encrypt(message)
    def Decrypt(self, message):
        return self.aes.decrypt(message)