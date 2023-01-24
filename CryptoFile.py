#!/usr/bin/env python3

import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7


class CryptoFile():
    def __init__(self) -> None:
        pass

#Method for deleting a file
    def removeFile(file):
        if os.path.isfile(file):
            os.remove(file)
        else:      
            print("Error: %s file not found" % file)

#Methode that generate RSA key
    def generate_RSA(bits:int=2048):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=bits
        )
        public_key = private_key.public_key()
        return private_key, public_key

#Method that export RSA key to PEM file
    def generateKeys():
        private,public = CryptoFile.generate_RSA()

        private_key_pem = private.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_key_pem = public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open("public.pem", "wb") as f:
                f.write(public_key_pem)

        with open("private.pem", "wb") as f:
                f.write(private_key_pem)

#Method that load private key from PEM string
    def loadPrivatekey(private_key_pem:str):
        private_key_pem = private_key_pem.encode('utf-8')
        private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None,
        backend=default_backend()
        )
        return private_key

#Method that load private key from PEM file
    def loadPrivatekeyFromFile(pemFile):
        with open(pemFile, "rb") as key_file:
            private_key_pem = key_file.read()
            private_key = serialization.load_pem_private_key(
            private_key_pem,
            password=None,
            backend=default_backend()
            )
        return private_key

#Method that load public key from PEM string
    def loadPublickey(public_key_pem:str):
        public_key_pem = public_key_pem.encode('utf-8')
        public_key = serialization.load_pem_public_key(
        public_key_pem,
        backend=default_backend()
        )
        return public_key

#Method that load public key from PEM file
    def loadPublickeyFromFile(pemFile):
        with open(pemFile, "rb") as key_file:
            public_key_pem = key_file.read()
            public_key = serialization.load_pem_public_key(
            public_key_pem,
            backend=default_backend()
            )
        return public_key
        
#Method for encrypting a file
    def encryptFile(file_name, public_key,rmFile = False):
        with open(file_name, "rb") as f:
            data = f.read()

        padder = PKCS7(algorithms.AES.block_size).padder()
        data = padder.update(data) + padder.finalize()

        # Generate a random AES key
        aes_key = os.urandom(32)

        # Encrypt the data with AES
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()

        # Encrypt the AES key with RSA
        aes_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        
        # Write the encrypted data and AES key to a new file
        with open(file_name + ".enc", "wb") as f:
            f.write(aes_key)
            f.write(iv)
            f.write(ciphertext)
        
        if rmFile:
            CryptoFile.removeFile(file_name)         

#Method for decrypting a file
    def decryptFile(file_name, private_key):
        with open(file_name, "rb") as f:
            aes_key = f.read(256)
            iv = f.read(16)
            plaintext = f.read()

        # Decrypt the AES key with RSA
        aes_key = private_key.decrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Decrypt the data with AES
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(plaintext) + decryptor.finalize()

        unpadder = PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(plaintext) + unpadder.finalize()

        # Write the decrypted data to a new file
        with open(file_name[:-4], "wb") as f:
            f.write(plaintext)

    