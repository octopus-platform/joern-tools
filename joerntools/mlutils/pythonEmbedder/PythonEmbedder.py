import os

from FeatureArray import FeatureArray
from FeatureArrayToMatrix import FeatureArrayToMatrix

class Embedder:
    
    def embed(self, directory):
        
        featureArray = self._createFeatureArray(directory)
        termDocMatrix = self._createTermDocumentMatrix(featureArray)
        termDocMatrix.tfidf()
        self._outputInLIBSVMFormat(termDocMatrix, directory)
        
    def _createFeatureArray(self, directory):
        
        featureArray = FeatureArray()
        
        dataDir = os.path.join(directory, 'data')
        filenames = os.listdir(dataDir)
        for f in filenames:
            label = f
            filename = os.path.join(dataDir, f)
            items = file(filename, 'r').readlines()
            featureArray.add(label, items)
        return featureArray
    
    def _createTermDocumentMatrix(self, featureArray):
        converter = FeatureArrayToMatrix()
        return converter.convertFeatureArray(featureArray)
    
    def _outputInLIBSVMFormat(self, termDocMatrix, directory):
        
        from scipy.sparse import csc_matrix
        m =  csc_matrix(termDocMatrix.matrix)
        nCols = m.shape[1]
        
        outFilename = os.path.join(directory, 'embedding.libsvm')
        outFile = file(outFilename, 'w')
        
        for i in xrange(nCols):
            label = termDocMatrix.index2Doc[i] 
            
            col = m.getcol(i)
            entries = [(i,col[i,0]) for i in col.indices]
            features = " ".join(['%d:%f' % e for e in entries])
            row = '%s %s #%s\n' % (label, features, label) 
            outFile.write(row)
        
        outFile.close()
        
if __name__ == '__main__':
    import sys
    embeder = Embedder()
    embeder.embed(sys.argv[1])
    