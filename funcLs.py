#!/usr/bin/env python2

import sys
from joern.all import JoernSteps
from ParseLocationString import parseLocationOrFail
from PipeTool import PipeTool

DESCRIPTION = """List the contents of a function. Expects
filename:startLine:startPos:startIndex:stopIndex lines"""

class FuncLs(PipeTool):
    
    def __init__(self):
        PipeTool.__init__(self, DESCRIPTION)
    
    # @Override
    def streamStart(self):
        self.j = JoernSteps()
        self.j.connectToDatabase()

    # @Override
    def processLine(self, line):
        x = parseLocationOrFail(line)
        filename = x[0]
        location = "%s:%s:%s:%s" % tuple(x[1:])
            
        query = """getFunctionByFilenameAndLoc("%s","%s")
        .sideEffect{ funcName = it.functionName; funcLoc = it.location }
        .id.transform{ "functionId: " + it}
        .queryToNodes()
        .transform{ [it.id, "%s", funcLoc, funcName, it.type, it.code] }
        
        """ % (filename, location, filename) 
        
        y = self.j.runGremlinQuery(query)
        for z in y:
            self.output('%s\t%s:%s\t%s\t%s\t%s\n' % tuple(z))
        

if __name__ == '__main__':
    tool= FuncLs()
    tool.run()
