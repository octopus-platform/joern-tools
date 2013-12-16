#!/usr/bin/env python2

from PipeTool import PipeTool
from mlutils.SallyLoader import SallyLoader
from sklearn.metrics.pairwise import pairwise_distances
import sys

DESCRIPTION = """ Calculate the k nearest neighbors to a data point
based on an embedding. """

DEFAULT_DIRNAME = 'embedding'
DEFAULT_K = 10

class KNN(PipeTool):
    
    def __init__(self):
        PipeTool.__init__(self, DESCRIPTION)
        self.loader = SallyLoader()
        
        self.argParser.add_argument('-k', '--k', nargs='?', type=int,
                                    help =""" number of nearest
                                    neighbors to determine""",
                                    default = DEFAULT_K)

        self.argParser.add_argument('-d', '--dirname', nargs='?',
                                    type = str, help="""The directory containing the embedding""",
                                    default = DEFAULT_DIRNAME)
        
        self.NNI = None

    def _loadEmbedding(self, dirname):
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
        if not self.emb.dExists():
            self.emb.D = self._calculateDistanceMatrix()
        
        if self.NNI == None:
            self.NNI = self.emb.D.argsort(axis=0)
            self.NNV = self.emb.D.copy()
            self.NNV.sort(axis=0)
    
        try:
            dataPointIndex = self.emb.rTOC[line]
        except KeyError:
            sys.stderr.write('Warning: no data point found for %s\n' %
                             (line))
        
        for i in self.NNI[0:self.args.k, dataPointIndex]:
            print self.emb.TOC[i]


    def _calculateDistanceMatrix(self):
        return pairwise_distances(self.emb.x, metric='cosine')

if __name__ == '__main__':
    tool = KNN()
    tool.run()
