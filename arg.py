#!/usr/bin/env python2

import sys, argparse
from joern.all import JoernSteps

class CLI():
    def __init__(self):
        self._initializeOptParser()
        self._parseCommandLine()
    
    def _initializeOptParser(self):
        self.argParser = argparse.ArgumentParser(description =\
        "Returns all n'th arguments of calls to the specified\
        callee.") 
        self.argParser.add_argument('callee', type=str)
        self.argParser.add_argument('n', type=str)
        self.argParser.add_argument('-s', '--symbols',
        action='store_true', help='return symbols used rather than\
        code.')
   
    def _parseCommandLine(self):
        self.args = self.argParser.parse_args()

    def run(self):
        
        j = JoernSteps()
        j.connectToDatabase()

        query = """
        getArgumentNTo("%s", "%d")
        .sideEffect{ code = it.code; node = it; }
        .astNodeToBasicBlock()
        .sideEffect{loc = it.location;}.transform{ node }
        """ % (sys.argv[1], int(sys.argv[2]) - 1)

        if self.args.symbols:
            query += """.astNodeToSymbolsUsed().sideEffect{code = it.code;
            }.transform{ node } """
        
        query += """
        .functionAndFilename().sideEffect{ (funcName, filename) = it }
        .transform{ [code, funcName, filename, loc] }
        """ 
    
        y = j.runGremlinQuery(query)
        for x in y:
            print '%s\t%s\t%s\t%s' % tuple(x)

if __name__ == '__main__':
    cli = CLI()
    cli.run()

