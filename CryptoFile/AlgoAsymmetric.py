from abc import ABC, abstractmethod
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization, hashes


class ILoadKeys(ABC):

    @abstractmethod
    def loadPublickeyFromFile(file):
        pass

    @abstractmethod
    def loadPrivatekeyFromFile(file):
        pass


class PEMFormat(ILoadKeys):

    def loadPublickeyFromFile(file):
        with open(file, "rb") as key_file:
            public_key_pem = key_file.read()
            public_key = serialization.load_pem_public_key(
                public_key_pem,
                backend=default_backend()
            )
        return public_key

    def loadPrivatekeyFromFile(file):
        with open(file, "rb") as key_file:
            private_key_pem = key_file.read()
            private_key = serialization.load_pem_private_key(
                private_key_pem,
                password=None,
                backend=default_backend()
            )
        return private_key


class DERFormat(ILoadKeys):
    pass


class IAsysmmetric(ABC):
    @abstractmethod
    def generateKeys(self):
        pass

    @abstractmethod
    def exportKeys(self):
        pass

    @abstractmethod
    def loadPublicKey(self):
        pass

    @abstractmethod
    def loadPrivateKey(self):
        pass

    @abstractmethod
    def encrypt(self):
        pass

    @abstractmethod
    def decrypt(self):
        pass


class RSA(IAsysmmetric):

    keys = {
        'privateKey': None,
        'publicKey': None
    }

    def __init__(self, publicExponent=65537, keySize=2048) -> None:
        super().__init__()
        self.publicExponent = publicExponent
        self.keySize = keySize

    def generateKeys(self):
        # Method that generate RSA key
        self.keys['privateKey'] = rsa.generate_private_key(
            public_exponent=self.publicExponent,
            key_size=self.keySize
        )
        self.keys['publicKey'] = self.keys['privateKey'].public_key()
        return self

    def exportKeys(self,folder=None):

        if not self.keys['privateKey'] and not self.keys['publicKey']:
            return

        privateKey_pem = self.keys['privateKey'].private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        publicKey_pem = self.keys['publicKey'].public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        if folder:
            with open(f"{folder}/public.pem", "wb") as f:
                f.write(publicKey_pem)

            with open(f"{folder}/private.pem", "wb") as f:
                f.write(privateKey_pem)
        else:
            with open(f"public.pem", "wb") as f:
                f.write(publicKey_pem)

            with open(f"private.pem", "wb") as f:
                f.write(privateKey_pem)

    def loadPublicKey(self, publicKey):
        self.keys['publicKey'] = publicKey
        return self
    
    def loadPrivateKey(self, privateKey):
        self.keys['privateKey'] = privateKey
        return self

    def encrypt(self, data):
        dataEnc = self.keys['publicKey'].encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return dataEnc

    def decrypt(self, dataEnc):
        data = self.keys['privateKey'].decrypt(
            dataEnc,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return data
