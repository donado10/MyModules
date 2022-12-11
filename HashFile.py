import hashlib
import os

#return True if a file is empty
def isFileEmpty(path):
    file = open(path,'rt')
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

    #method for hashing a file
    def hashFile(self,filename):
        with open(self.sourceFile+filename,'rb') as f:
            toHash = f.read()
            result = hashlib.md5(str(toHash).encode())
        return result

    #return True if two hashs are equals
    def isHashsEqual(self,filename):
        if isFileEmpty(self.hashStore):
            return False 

        result = self.hashFile(filename)

        if self.getHashInStore() == result.hexdigest():
            return True
        return False

    #method to get the hash in the store
    def getHashInStore(self):
        hashInStore = open(self.hashStore,'rt')        

        for hashfile in hashInStore:
            getHashStore = hashfile
        hashInStore.close()

        return getHashStore

    #method for saving an hash in a file
    def saveHash(self,hashResult):
        hashStorage = open(self.hashStore,'w')
        hashStorage.write(hashResult.hexdigest())
        hashStorage.close()