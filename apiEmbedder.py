#!/usr/bin/env python

from argparse import ArgumentParser
from joerntools.DBInterface import DBInterface
import os
import sys

from sklearn.metrics.pairwise import pairwise_distances
from joerntools.mlutils.sallyEmbedder.SallyBasedEmbedder import SallyBasedEmbedder

description = """apiEmbedder.py - A tool to embed code in vector spaces"""

DEFAULT_DIRNAME = 'embedding'

class APIEmbedder(object):
    
    def __init__(self):
        self.description = description
        self._initializeOptParser()
        self._initializeDBConnection()
    
    def _initializeOptParser(self):
        self.argParser = ArgumentParser(description = self.description)
        
        self.argParser.add_argument('-d', '--dirname', nargs='?',
                                    type = str, help="""The directory to write the embedding to.""",
                                    default = DEFAULT_DIRNAME)
    
    def _initializeDBConnection(self):
        self.dbInterface = DBInterface()
    
    
    def run(self):
        self._parseCommandLine()
        self._initializeOutputDirectory()
        self._connectToDatabase()
        
        functions = self._getAPISymbolsFromDatabase()
        self._writeDataPoints(functions)
        self._finalizeOutputDirectory()
    
        self._embed()
                
    
    def _embed(self):
        self.embedder = SallyBasedEmbedder()
        self.embedder.embed(self.args.dirname)
    
    def _connectToDatabase(self):
        self.dbInterface.connectToDatabase()
    
    def _parseCommandLine(self):
        self.args = self.argParser.parse_args()
    
    def _writeDataPoints(self, functions):
        
        for (funcId, symbols) in functions:
            self.toc.write("%d\n" % (funcId))
            self._addDataPoint(symbols)
    
    def _addDataPoint(self, symbols):
        datapointFilename = os.path.join(self.dataDir, str(self.curDatapoint))
        f = file(datapointFilename, 'w')
        f.writelines([x + "\n" for x in symbols])
        f.close()
        self.curDatapoint += 1

    def _initializeOutputDirectory(self):
        directory = self.args.dirname
        if os.path.exists(directory):
            print 'Output directory exists. Aborting.'
            sys.exit()
        
        self.dataDir = os.path.join(directory, 'data') 
        self.tocFilename = os.path.join(directory, 'TOC') 
        os.makedirs(self.dataDir)
        self.toc = file(self.tocFilename, 'w')
        
        self.curDatapoint = 0
        
    def _finalizeOutputDirectory(self):
        self.toc.close()

    def _getAPISymbolsFromDatabase(self):
        
        # Fetch all API symbols in a single query. Might be
        # smarter to split this into multiple queries for large
        # codebases.
        
        query = """
        queryNodeIndex('type:Function').sideEffect{funcId = it.id}
        .transform{ [funcId, it.functionToAPISymbolNodes().code.toList()] }
        """
        return self._runGremlinQuery(query)
        
 
    def _runGremlinQuery(self, query):
        return self.dbInterface.runGremlinQuery(query)


if __name__ == '__main__':
    embedder = APIEmbedder()
    embedder.run()