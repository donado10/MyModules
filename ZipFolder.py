import shutil
from datetime import datetime

class ZipFolder:


    def __init__(self, source,destination) -> None:
        self.source = source
        self.destination = destination

    def getDate(self):
        now = datetime.now()
        return now.strftime("%d-%m-%Y_%H-%M-%S")
    
    def buildZipFile(self,fileName):
        try:
            self.date = self.getDate()

            test = shutil.make_archive(self.destination + fileName, 'zip', self.source)
            return True           
        except:
            return False

    def copyZipFile(self,source,destination):
        try:
            shutil.copy(source, destination)
            return True
        except:
            return False
            
