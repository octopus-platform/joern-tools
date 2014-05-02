
from joerntools.mlutils.EmbeddingLoader import EmbeddingLoader
from joerntools.mlutils.EmbeddingSaver import EmbeddingSaver
from sklearn.metrics.pairwise import pairwise_distances


class KNN():
    def __init__(self):
        self.loader = EmbeddingLoader()
        self.saver = EmbeddingSaver() 

    
    def setEmbeddingDir(self, dirname):
        self.dirname = dirname
    
    def setLimitArray(self, limit):
        self.limit = limit
    
    def setK(self, k):
        self.k = k
    
    def setNoCache(self, no_cache):
        self.no_cache = no_cache
    
    def initialize(self):
        
        self.emb = self._loadEmbedding(self.dirname)
        if self.limit:
            self._loadValidNeighbors()


    def _loadEmbedding(self, dirname):
        self.saver.setEmbeddingDir(dirname)
        return self.loader.load(dirname, tfidf=False, svd_k=0)
        

    def _loadValidNeighbors(self):
        self.validNeighbors = self.limit

    
    def getNeighborsFor(self, line):
        self.calculateDistances()
        
        dataPointIndex = self.emb.rTOC[line]    
        nReturned = 0
            
        neighbors = []
            
        for i in self.emb.NNI[:, dataPointIndex]:
            
            if self.limit:
                if not self.emb.TOC[i] in self.validNeighbors:
                    continue

            neighbors.append(self.emb.TOC[i])
            nReturned += 1
            
            if nReturned == self.k:
                break

        return neighbors
    
    def calculateDistances(self):
        if not self.emb.dExists():
            self.emb.D = self._calculateDistanceMatrix()
     
            if not self.no_cache:
                self.saver.saveDistanceMatrix(self.emb)
            
        if not self.emb.nnExists():
            self._calculateNearestNeighbors()
            if not self.no_cache:
                self.saver.saveNearestNeighbors(self.emb)
            
    def _calculateNearestNeighbors(self):
        self.emb.NNV = self.emb.D.copy()
        self.emb.NNI = self.emb.D.argsort(axis=0)
        self.emb.NNV.sort(axis=0)
        
    def _calculateDistanceMatrix(self):
        return pairwise_distances(self.emb.x, metric='cosine')