#!/usr/bin/env python2

import sys, os
from DemuxTool import DemuxTool

DESCRIPTION = """Split file into different files using the first field
of each line as a key and create a table of contents. This is like
"awk -F, '{print > $1}' file1" but in cases where the key cannot be
used as a filename."""

DEFAULT_DATA_DIR = 'data_dir'

class Demux(DemuxTool):
    def __init__(self):
        DemuxTool.__init__(self, DESCRIPTION)
        self._initializeDefaults()
        
    def _initializeDefaults(self):
        self.currentFileNum = 0
        self.keyToFilename = dict()
        self.dataDir = DEFAULT_DATA_DIR

    # @Override
    def streamStart(self):
        self._createDataDir()

    def _createDataDir(self):
        try:
            os.makedirs(self.dataDir + '/data/')
        except OSError:
            pass

        self.toc = file(self.dataDir + '/TOC', 'w')
    
    # @ Override
    def processLines(self):
        curKey = self.lines[0].split('\t')[0]
        
        f = self._openOutputFile(curKey)
        
        for line in self.lines:
            line = line.rstrip()
            record = line.split('\t')
            f.write('\t'.join(record[1:]) + '\n')
        f.close()
    
    def _openOutputFile(self, curKey):
        
        if curKey in self.keyToFilename:
            filename = self.keyToFilename[curKey]
        else:
            filename = self.dataDir + '/data/' + str(self.currentFileNum)
            self.currentFileNum += 1
            self.keyToFilename[curKey] = filename
            self.toc.write(curKey + '\n')

        return file(filename, 'a')

    # @Override
    def streamEnd(self):
        self.toc.close()

if __name__ == '__main__':
    tool = Demux()
    tool.run()
