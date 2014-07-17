
import os

class MLDataDir:
    
    def __init__(self):

        self.curDatapoint = 0

    def create(self, directory):
        
        self.dataDir = os.path.join(directory, 'data') 
        self.tocFilename = os.path.join(directory, 'TOC') 
        os.makedirs(self.dataDir)
        self.toc = file(self.tocFilename, 'w')

    def addDataPoint(self, funcId, symbols):
        
        self.toc.write("%d\n" % (funcId))

        datapointFilename = os.path.join(self.dataDir, str(self.curDatapoint))
        f = file(datapointFilename, 'w')
        f.writelines([str(x) + "\n" for x in symbols])
        f.close()
        self.curDatapoint += 1
    
    def finalize(self):
        self.toc.close()
    
