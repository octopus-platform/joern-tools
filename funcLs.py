#!/usr/bin/env python2

import sys, argparse
from joern.all import JoernSteps
from ParseLocationString import parseLocationString

class CLI():
    def __init__(self):
        self._initializeOptParser()
        self._parseCommandLine()
    
    def _initializeOptParser(self):
        self.argParser = argparse.ArgumentParser(description = """
        For a location pointing to a function, list different
        properties of the function such as callees, type or symbol
        usage. By default, output the function signature.""")
 
    
    def _parseCommandLine(self):
        self.args = self.argParser.parse_args()

    def run(self):
        
        j = JoernSteps()
        j.connectToDatabase()
        
        for line in sys.stdin:
            try:
                (filename, startLine, stopLine, startIndex, stopIndex)\
                    = parseLocationString(line[:-1])
            except ValueError:
                print 'Invalid location line.'
                self.usage()
                sys.exit()

            query = """
            getFunctionByFilenameAndLoc("%s","%s")
            """ % (filename, location) 
        
            query += '.signature'

            y = j.runGremlinQuery(query)
            for x in y:
                print x

if __name__ == '__main__':
    cli = CLI()
    cli.run()
