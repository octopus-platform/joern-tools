#!/usr/bin/env python2

from PipeTool import PipeTool
from mlutils.EmbeddingLoader import EmbeddingLoader
from mlutils.EmbeddingSaver import EmbeddingSaver
from sklearn.metrics.pairwise import pairwise_distances
import sys

DESCRIPTION = """ Calculate the k nearest neighbors to a data point
based on an embedding. """

DEFAULT_DIRNAME = 'embedding'
DEFAULT_K = 10

class KNN(PipeTool):
    
    def __init__(self):
        PipeTool.__init__(self, DESCRIPTION)
        self.loader = EmbeddingLoader()
        self.saver = EmbeddingSaver()

        self.argParser.add_argument('-k', '--k', nargs='?', type=int,
                                    help =""" number of nearest
                                    neighbors to determine""",
                                    default = DEFAULT_K)

        self.argParser.add_argument('-d', '--dirname', nargs='?',
                                    type = str, help="""The directory containing the embedding""",
                                    default = DEFAULT_DIRNAME)

        self.argParser.add_argument('-n', '--no-cache',
                                    action='store_false', default=True,
                                    help= """Cache calculated
                                    distances on disk. """)

    def _loadEmbedding(self, dirname):
        self.saver.setEmbeddingDir(dirname)
        try:
            return self.loader.load(dirname)
        except IOError:
            sys.stderr.write('Error reading embedding.\n')
            sys.exit()

    # @Override
    def streamStart(self):
        self.emb = self._loadEmbedding(self.args.dirname)

    # @Override
    def processLine(self, line):
        self.calculateDistances()
        
        try:
            dataPointIndex = self.emb.rTOC[line]
        except KeyError:
            sys.stderr.write('Warning: no data point found for %s\n' %
                             (line))
        
        for i in self.emb.NNI[0:self.args.k, dataPointIndex]:
            print self.emb.TOC[i]


    def calculateDistances(self):
        if not self.emb.dExists():
            self.emb.D = self._calculateDistanceMatrix()
            if self.args.cache:
                self.saver.saveDistanceMatrix(self.emb)
            
        if not self.emb.nnExists():
            self._calculateNearestNeighbors()
            if self.args.cache:
                self.saver.saveNearestNeighbors(self.emb)
            
    def _calculateNearestNeighbors(self):
        self.emb.NNI = self.emb.D.argsort(axis=0)
        self.emb.NNV = self.emb.D.copy()
        self.emb.NNV.sort(axis=0)

    def _calculateDistanceMatrix(self):
        return pairwise_distances(self.emb.x, metric='cosine')
        

if __name__ == '__main__':
    tool = KNN()
    tool.run()
