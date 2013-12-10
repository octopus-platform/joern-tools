#!/usr/bin/env python2

import sys, argparse
from joern.all import JoernSteps
from ParseLocationString import ParseLocationString

class CLI():
    def __init__(self):
        self._initializeOptParser()
        self._parseCommandLine()
    
    def _initializeOptParser(self):
        self.argParser = argparse.ArgumentParser(description = """
        For a location pointing to a function, list different
        properties of the function such as callees, type or symbol
        usage. By default, output the function signature.""")
 
        self.argParser.add_argument('location', action=ParseLocationString)

    def _parseCommandLine(self):
        self.args = self.argParser.parse_args()

    def run(self):
        
        j = JoernSteps()
        j.connectToDatabase()
        
        query = """
        getFunctionByFilenameAndLoc("%s","%s")
         """ % (self.args.filename, self.args.location) 
        
        query += '.signature'

        y = j.runGremlinQuery(query)
        for x in y:
            print x

if __name__ == '__main__':
    cli = CLI()
    cli.run()
