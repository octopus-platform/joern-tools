#!/usr/bin/env python2

import sys, argparse
from joern.all import JoernSteps
from ParseLocationString import ParseLocationString

class CLI():
    def __init__(self):
        self._initializeOptParser()
        self._parseCommandLine()
    
    def _initializeOptParser(self):
        self.argParser = argparse.ArgumentParser(description =\
        "Print code at given file and location where location is\
        filename:startLine:stopLine:startIndex:stopIndex as saved in\
        the location attribute of database nodes.")
 
        self.argParser.add_argument('location', action=ParseLocationString)
        
    def _parseCommandLine(self):
        self.args = self.argParser.parse_args()

    def run(self):
     
        try:
            f = file(self.args.filename)
        except IOError:
            sys.stderr.write('Error: %s: no such file or directory\n'
                             % self.args.filename)
            sys.exit()

        f.seek(self.args.startIndex)
        content = f.read(self.args.stopIndex - self.args.startIndex + 1)
        f.close()
        
        print content

if __name__ == '__main__':
    cli = CLI()
    cli.run()
