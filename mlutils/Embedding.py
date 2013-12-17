
class Embedding:
    def __init__(self):
        self.x, self.y = None, None
        self.TOC = []
        self.rTOC = dict()
        self.featTable = dict()
        self.rFeatTable = dict()
        
        self.D = None
        self.NNI = None
        self.NNV = None

    def dExists(self):
        return (self.D != None)
    
    def nnExists(self):
        return (self.NNI != None)
        
