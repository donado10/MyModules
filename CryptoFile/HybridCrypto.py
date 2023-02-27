from abc import ABC, abstractmethod
from CryptoFile.AlgoSymmetric import AESCBC, AESOFB, AESCTR, AESCFB, AESECB
from CryptoFile.AlgoAsymmetric import RSA


class AbstractFactory(ABC):
    @abstractmethod
    def generateAsymmetric():
        pass

    @abstractmethod
    def generateSymmetric():
        pass


class AESplusRSA(AbstractFactory):
    def generateSymmetric(mode: str = "CBC"):

        if mode.upper() == "CBC":
            return AESCBC()

        if mode.upper() == "OFB":
            return AESOFB()

        if mode.upper() == "CTR":
            return AESCTR()

        if mode.upper() == "CFB":
            return AESCFB()

        if mode.upper() == "ECB":
            return AESECB()

    def generateAsymmetric():
        return RSA()
