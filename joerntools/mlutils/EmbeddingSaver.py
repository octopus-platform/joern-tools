
import cPickle as pickle
from Embedding import *
import h5py

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
        
        f = h5py.File(filename, 'w')
        f.create_dataset('distanceM', data=emb.NNI)
        f.close()
        
