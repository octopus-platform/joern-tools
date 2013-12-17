
import cPickle as pickle
from Embedding import *

class EmbeddingSaver:

    def __init__(self):
        pass
    
    def setEmbeddingDir(self, dirname):
        self.dirname = dirname

    def saveDistanceMatrix(self, emb):
        filename = self.dirname + D_FILENAME
        pickle.dump(emb.D, file(filename, 'w'))

    def saveNearestNeighbors(self, emb):
        filename = self.dirname + NNI_FILENAME
        pickle.dump(emb.NNI, file(filename, 'w'))

        filename = self.dirname + NNV_FILENAME
        pickle.dump(emb.NNV, file(filename, 'w'))
        
