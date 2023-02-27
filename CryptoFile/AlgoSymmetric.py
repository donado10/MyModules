import os
from abc import ABC, abstractmethod
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7


class ISymmetric(ABC):

    @abstractmethod
    def encrypt(self, data):
        pass

    @abstractmethod
    def decrypt(self, cipherData):
        pass


class Nonce():
    def generateNonce(self, nonceLength=16):
        self.nonce = os.urandom(nonceLength)
        return self


class AES(ISymmetric):

    secret = None

    def __init__(self) -> None:
        super().__init__()

    def paddingData(data):
        padder = PKCS7(algorithms.AES.block_size).padder()
        dataAfterPadding = padder.update(data) + padder.finalize()
        return dataAfterPadding

    def unpaddingData(data):
        unpadder = PKCS7(algorithms.AES.block_size).unpadder()
        dataUnpadding = unpadder.update(data) + unpadder.finalize()
        return dataUnpadding

    def generateSecret(self, secretLength=32):
        self.secret = os.urandom(secretLength)
        return self

    def encrypt(self):
        pass

    def decrypt(self):
        pass


class AESCBC(AES):
    description = {
        'secret': True,
        'nonce': True
    }

    def __init__(self) -> None:
        super().__init__()
        self.nonce = None

    def generateNonce(self):
        self.nonce = Nonce.generateNonce()

    def encrypt(self, data):
        dataPadding = AES.paddingData(data)
        cipher = Cipher(algorithms.AES(self.secret),
                        modes.CBC(self.nonce), default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(dataPadding) + encryptor.finalize()
        return ciphertext

    def decrypt(self, cipherData):
        cipher = Cipher(algorithms.AES(self.secret),
                        modes.CBC(self.nonce), default_backend())
        decryptor = cipher.decryptor()
        data = decryptor.update(cipherData) + decryptor.finalize()
        dataUnpadding = AES.unpaddingData(data)
        return dataUnpadding


class AESOFB(AES):
    description = {
        'secret': True,
        'nonce': True
    }

    def __init__(self) -> None:
        super().__init__()
        self.nonce = None

    def generateNonce(self):
        self.nonce = Nonce.generateNonce()

    def encrypt(self, data):
        dataPadding = AES.paddingData(data)
        cipher = Cipher(algorithms.AES(self.secret),
                        modes.OFB(self.nonce), default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(dataPadding) + encryptor.finalize()
        return ciphertext

    def decrypt(self, cipherData):
        cipher = Cipher(algorithms.AES(self.secret),
                        modes.OFB(self.nonce), default_backend())
        decryptor = cipher.decryptor()
        data = decryptor.update(cipherData) + decryptor.finalize()
        dataUnpadding = AES.unpaddingData(data)
        return dataUnpadding


class AESCTR(AES):
    description = {
        'secret': True,
        'nonce': True
    }

    def __init__(self) -> None:
        super().__init__()
        self.nonce = None

    def generateNonce(self):
        self.nonce = Nonce.generateNonce()

    def encrypt(self, data):
        dataPadding = AES.paddingData(data)
        cipher = Cipher(algorithms.AES(self.secret),
                        modes.CTR(self.nonce), default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(dataPadding) + encryptor.finalize()
        return ciphertext

    def decrypt(self, cipherData):
        cipher = Cipher(algorithms.AES(self.secret),
                        modes.CTR(self.nonce), default_backend())
        decryptor = cipher.decryptor()
        data = decryptor.update(cipherData) + decryptor.finalize()
        dataUnpadding = AES.unpaddingData(data)
        return dataUnpadding


class AESCFB(AES):
    description = {
        'secret': True,
        'nonce': True
    }

    def __init__(self) -> None:
        super().__init__()
        self.nonce = None

    def generateNonce(self):
        self.nonce = Nonce.generateNonce()

    def encrypt(self, data):
        dataPadding = AES.paddingData(data)
        cipher = Cipher(algorithms.AES(self.secret),
                        modes.CFB(self.nonce), default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(dataPadding) + encryptor.finalize()
        return ciphertext

    def decrypt(self, cipherData):
        cipher = Cipher(algorithms.AES(self.secret),
                        modes.CFB(self.nonce), default_backend())
        decryptor = cipher.decryptor()
        data = decryptor.update(cipherData) + decryptor.finalize()
        dataUnpadding = AES.unpaddingData(data)
        return dataUnpadding


class AESECB(AES):
    description = {
        'secret': True,
        'nonce': False
    }

    def __init__(self) -> None:
        super().__init__()

    def encrypt(self, data):
        dataPadding = AES.paddingData(data)
        cipher = Cipher(algorithms.AES(self.secret),
                        modes.ECB(), default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(dataPadding) + encryptor.finalize()
        return ciphertext

    def decrypt(self, cipherData):
        cipher = Cipher(algorithms.AES(self.secret),
                        modes.ECB(), default_backend())
        decryptor = cipher.decryptor()
        data = decryptor.update(cipherData) + decryptor.finalize()
        dataUnpadding = AES.unpaddingData(data)
        return dataUnpadding
