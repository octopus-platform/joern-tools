#!/usr/bin/env python2

import sys, argparse
from joern.all import JoernSteps
from ParseLocationString import parseLocationOrFail

class CLI():
    def __init__(self):
        self._initializeOptParser()
        self._parseCommandLine()
    
    def _initializeOptParser(self):
        self.argParser = argparse.ArgumentParser(description = """
        Read filename:startLine:startPos:startIndex:stopIndex from
        standard input and output the respective code.""")
        
    def _parseCommandLine(self):
        self.args = self.argParser.parse_args()

    def usage(self):
        self.argParser.print_help()
    
    def openFileOrFail(self, filename):
        try:
            f = file(filename)
        except IOError:
            sys.stderr.write('Error: %s: no such file or directory\n'
                             % filename)
            sys.exit()
        return f


    def run(self):
     
        for line in sys.stdin:
            (filename, startLine, startPos, startIndex, stopIndex)\
                = parseLocationOrFail(line)
                                                                    
            f = self.openFileOrFail(filename)
            f.seek(startIndex)
            content = f.read(stopIndex - startIndex + 1)
            f.close()
            print content

if __name__ == '__main__':
    cli = CLI()
    cli.run()
