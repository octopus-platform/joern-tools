#!/usr/bin/env python2

from sklearn.datasets import load_svmlight_file
from gzip import GzipFile

LEN_BIN = len(' bin=')

class SallyLoader:
    
    def __init__(self):
        self.x, self.y = None, None
        self.TOC = []
        self.featTable = dict()
        self.rFeatTable = dict()

    def load(self, dirname):
        self.dirname = dirname
        self.x, self.y = load_svmlight_file(dirname + '/embedding.libsvm')
        
        self._loadFeatureTable()
        self.loadTOC()

    def _loadFeatureTable(self):
        
        filename = self.dirname + '/feats.gz'
        f  = GzipFile(filename)
        
        # discard first line
        f.readline()

        while True:
            line = f.readline().rstrip()
            if line == '': break
            
            (feat, n) = self._parseHashTableLine(line)
            
            self.featTable[feat] = n
            self.rFeatTable[n] = feat
            
        f.close()
    
    def _parseHashTableLine(self, line):
        n, feat = line[LEN_BIN+1:].split(':')
        n = int(n , 16)
        feat = feat.lstrip().rstrip()
        return (feat, n)

    def loadTOC(self):
        filename = self.dirname + '/TOC'
        f = file(filename)
        self.TOC = f.readlines()
        f.close()
        
if __name__ == '__main__':
    import sys
    s = SallyLoader()
    s.load(sys.argv[1])
    
