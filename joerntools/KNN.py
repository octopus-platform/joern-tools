
from joerntools.mlutils.EmbeddingLoader import EmbeddingLoader
from sklearn.metrics.pairwise import pairwise_distances


class KNN():
    def __init__(self):
        self.loader = EmbeddingLoader()
    
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

    def _loadEmbedding(self, dirname):
        return self.loader.load(dirname, tfidf=False, svd_k=0)
        
    
    def getNeighborsFor(self, funcId):
        
        dataPointIndex = self.emb.rTOC[funcId]    
        nReturned = 0

        if self.limit:
            validNeighborIds = [dataPointIndex] + self.limit
            
            validNeighbors = [self.emb.rTOC[x] for x in self.limit]
            validNeighbors = [dataPointIndex] +  validNeighbors
            
            X = self.emb.x[validNeighbors, :]
            D = pairwise_distances(X, metric='cosine')
            NNI = list(D[0,:] .argsort(axis=0))[:self.k]
            return [validNeighborIds[x] for x in NNI]
        else:
            X = self.emb.x
            D = pairwise_distances(X, metric='cosine')
            NNI = list(D[dataPointIndex,:].argsort(axis=0))[:self.k]
            return [self.emb.TOC[x] for x in NNI]

    def calculateDistances(self):
        
        self.emb.D = self._calculateDistanceMatrix()
        self._calculateNearestNeighbors()
        
    def _calculateNearestNeighbors(self):
        self.emb.NNI = self.emb.D.argsort(axis=0)
        
    def _calculateDistanceMatrix(self):
        return pairwise_distances(self.emb.x, metric='cosine')
