#!/usr/bin/env python2

import sys
from joern.all import JoernSteps
from ParseLocationString import parseLocationOrFail
from PipeTool import PipeTool

DESCRIPTION = """For a location pointing to a function, list
different properties of the function such as callees, type or symbol
usage. By default, output the function signature."""

class FuncLs(PipeTool):
    
    def __init__(self):
        PipeTool.__init__(self, DESCRIPTION)
        
        self.argParser.add_argument('-c', '--calls',
                action='store_true', help='list calls.')
    
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
        """ % (filename, location) 
            
        if self.args.calls:
            query += """.id.transform{ "type:CallExpression AND functionId: " + it}
            .queryToNodes().outE().filter{it.n == '0'}.inV().sideEffect{callee = it.code;}
            .astNodeToBasicBlock().sideEffect{loc = it.location}.id
            .transform{ [funcName, "%s", funcLoc, loc, callee] }
            """ % (filename)
            y = self.j.runGremlinQuery(query)
            for z in y: print '%s\t%s\t%s\t%s\t%s' % tuple(z)
        else:
            query += '.transform{ [funcName, "%s", funcLoc, it.signature] }' % (filename)
            y = self.j.runGremlinQuery(query)
            for z in y:
                print '%s\t%s\t%s\t%s' % tuple(z)

if __name__ == '__main__':
    tool= FuncLs()
    tool.run()
