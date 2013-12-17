#!/usr/bin/env python2

from sklearn.datasets import load_svmlight_file
from gzip import GzipFile
from Embedding import *
import cPickle as pickle
import os

LEN_BIN = len(' bin=')

class EmbeddingLoader:
    
    def __init__(self):
        self.emb = Embedding()
        
    def load(self, dirname):
        self.dirname = dirname
        self.emb.x, self.emb.y = load_svmlight_file(dirname + EMBEDDING_FILENAME)
        
        self._loadFeatureTable()
        self._loadTOC()
        self._loadDistances()
        return self.emb
    
    def _loadFeatureTable(self):
        
        filename = self.dirname + FEATURE_FILENAME
        f  = GzipFile(filename)
        
        # discard first line
        f.readline()

        while True:
            line = f.readline().rstrip()
            if line == '': break
            
            (feat, n) = self._parseHashTableLine(line)
            
            self.emb.featTable[feat] = n
            self.emb.rFeatTable[n] = feat
            
        f.close()
    
    def _parseHashTableLine(self, line):
        n, feat = line[LEN_BIN+1:].split(':')
        n = int(n , 16)
        feat = feat.lstrip().rstrip()
        return (feat, n)

    def _loadTOC(self):
        filename = self.dirname + TOC_FILENAME
        f = file(filename)
        TOCLines = [x.rstrip() for x in f.readlines()]
        f.close()
        
        for i in range(len(self.emb.y)):
            label = self.emb.y[i]
            name = TOCLines[int(label)]
            self.emb.rTOC[name] = i
            self.emb.TOC.append(name)

    def _loadDistances(self):
        
        dFilename = self.dirname + D_FILENAME
        if os.path.exists(dFilename):
           self.emb.D = pickle.load(file(dFilename))

        nniFilename = self.dirname + NNI_FILENAME
        nnvFilename = self.dirname + NNV_FILENAME
        
        if os.path.exists(nniFilename):
            self.emb.NNI = pickle.load(file(nniFilename))
            self.emb.NNV = pickle.load(file(nnvFilename))
        

if __name__ == '__main__':
    import sys
    s = SallyLoader()
    s.load(sys.argv[1])
    
