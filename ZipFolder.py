import shutil
from datetime import datetime


class ZipFolder:

    source = None #Location for the source file to Zip
    destination = None #Destination for the new zip file

    def __init__(self, source,destination) -> None:
        self.source = source
        self.destination = destination
 
    #method to build a zip file
    def buildZipFile(self,fileName):
        try:
            shutil.make_archive(self.destination + fileName, 'zip', self.source)
            return True           
        except:
            return False

    #method to copy a zip file
    def copyZipFile(self,source,destination):
        try:
            shutil.copy(source, destination)
            return True
        except:
            return False
            
