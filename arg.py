#!/usr/bin/env python2

import sys
from joern.all import JoernSteps
from PipeTool import PipeTool

DESCRIPTION = """ Returns all n'th arguments of calls to the specified
callee. Accepts callee TAB $i lines on stdin where $i is the argument
index."""

class ArgTool(PipeTool):
    def __init__(self):
        PipeTool.__init__(self, DESCRIPTION)

        self.argParser.add_argument('-s', '--symbols',
                                    action='store_true', help='return\
                                    symbols used rather than code.')
    # @Override
    def streamStart(self):
        self.j = JoernSteps()
        self.j.connectToDatabase()

    # @Override
    def processLine(self, line):
        query = self._constructQueryForLine(line)
        
        y = self.j.runGremlinQuery(query)
        for x in y:
            print '%s\t%s\t%s\t%s' % tuple(x)
    
    def _constructQueryForLine(self, line):
        
        (callee, i) = self._readCalleeAndIOrFail(line)

        query = """
        getArgumentNTo("%s", "%d")
        .sideEffect{ code = it.code; node = it; }
        .astNodeToBasicBlock()
        .sideEffect{loc = it.location;}.transform{ node }
        """ % (callee, i)
        
        if self.args.symbols:
            query += """.astNodeToSymbolsUsed().sideEffect{code = it.code;
            }.transform{ node } """
            
        query += """
        .functionAndFilename().sideEffect{ (funcName, filename) = it }
        .transform{ [code, funcName, filename, loc] }
        """ 
        return query
        
    def _readCalleeAndIOrFail(self, line):
        try:
            (callee, i) = line.split('\t')
            i = int(i) - 1
        except ValueError:
            self.argParser.print_help()
            sys.exit()
        return (callee, i)

if __name__ == '__main__':
    tool = ArgTool()
    tool.run()
