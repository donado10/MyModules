import hashlib
import os

def isFileEmpty(path):
    file = open(path,'rt')
    file.seek(0, os.SEEK_END)
    if file.tell() == 0:
        file.close()
        return True
    file.close()
    return False


class HashFile:

    sourceFile = None
    hashDB = None
    
    def __init__(self,sourceFile,hashDB) -> None:
        self.sourceFile = sourceFile
        self.hashDB = hashDB

    def saveHash(self,hash):
        DB = open(self.hashDB,'w')
        DB.write(hash.hexdigest())
        DB.close()

    def hashFile(self,filename):
        with open(self.sourceFile+filename,'rb') as f:
            toHash = f.read()
            result = hashlib.md5(str(toHash).encode())
        return result

    def isHashsEqual(self,filename):

        if isFileEmpty(self.hashDB,):
            return False 

        result = self.hashFile(filename)
        database = open(self.hashDB,'rt')
        
        for hashfile in database:
            getHashDB = hashfile
        database.close()

        if getHashDB == result.hexdigest():
            return True
        return False