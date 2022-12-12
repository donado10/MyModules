import hashlib
import os

#function that return True if a file is empty
def isFileEmpty(filePath):
    file = open(filePath,'rt')
    file.seek(0, os.SEEK_END)
    if file.tell() == 0:
        file.close()
        return True
    file.close()
    return False


class HashFile:
    sourceFile = None #Location for the file to hash
    hashStore = None #Location to store the hash
    
    def __init__(self,sourceFile,hashStore) -> None:
        self.sourceFile = sourceFile
        self.hashStore = hashStore

    #method for hashing a file with md5
    def hashFile(self,filename):
        with open(self.sourceFile+filename,'rb') as file:
            toHash = file.read()
            result = hashlib.md5(str(toHash).encode())
        return result

    #method that return True if the new hash of the file and the hash in the store are equals
    def isHashsEqual(self,filename):
        if isFileEmpty(self.hashStore):
            return False 

        result = self.hashFile(filename)

        if self.getHashInStore() == result.hexdigest():
            return True
        return False

    #method to get the hash value from the hash store
    def getHashInStore(self):
        hashInStore = open(self.hashStore,'rt')        

        for currentHash in hashInStore:
            getHashStore = currentHash
        hashInStore.close()

        return getHashStore

    #method for saving an hash in the hash store
    def saveHash(self,hashResult):
        hashStorage = open(self.hashStore,'w')
        hashStorage.write(hashResult.hexdigest())
        hashStorage.close()