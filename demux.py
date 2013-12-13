#!/usr/bin/env python2

import sys, os
from PipeTool import PipeTool

DESCRIPTION = """Split file into different files using the first field
of each line as a key and creates a table of contents. This is like
"awk -F, '{print > $1}' file1" but in cases where the key cannot be
used as a filename."""

DEFAULT_DATA_DIR = 'data_dir'

class Demux(PipeTool):
    def __init__(self):
        PipeTool.__init__(self, DESCRIPTION)
        self._initializeDefaults()
        
    def _initializeDefaults(self):
        self.currentFile = None
        self.currentFilename = ''
        self.currentFileNum = 0
        self.keyToFilename = dict()
        self.dataDir = DEFAULT_DATA_DIR

    def streamStart(self):
        self._createDataDir()

    def _createDataDir(self):
        try:
            os.makedirs(self.dataDir + '/data/')
        except OSError:
            pass

        self.toc = file(self.dataDir + '/TOC', 'w')
        
    # @Override
    def processLine(self, line):
        record = line.split('\t')
        if(len(record) < 2 ):
            sys.stderr.write('Warning: input line does not contain key\n')
            return
        
        filename = record[0]
        if filename != self.currentFilename:
            self._closeCurrentFile()
            self.currentFilename = filename            
            self._openOutputFile()

        self.currentFile.write('\t'.join(record[1:]) + '\n')
    
    def _closeCurrentFile(self):
        if self.currentFile != None:
            self.currentFile.close()
    
    def _openOutputFile(self):
        if self.currentFilename in self.keyToFilename:
            filename = self.keyToFilename[self.currentFilename]
        else:
            filename = self.dataDir + '/data/' + str(self.currentFileNum)
            self.currentFileNum += 1
            self.keyToFilename[self.currentFilename] = filename
            self.toc.write(self.currentFilename + '\n')

        self.currentFile = file(filename, 'w')

    # @Override
    def streamEnd(self):
        if self.currentFile != None:
            self.currentFile.close()
        self.toc.close()

if __name__ == '__main__':
    tool = Demux()
    tool.run()
