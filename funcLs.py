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
        For a location pointing to a function, list different
        properties of the function such as callees, type or symbol
        usage. By default, output the function signature.""")
     
        self.argParser.add_argument('-c', '--calls',
            action='store_true', help='list calls.')
        
    def _parseCommandLine(self):
        self.args = self.argParser.parse_args()

    def run(self):
        
        j = JoernSteps()
        j.connectToDatabase()
        
        for line in sys.stdin:
            
            x = parseLocationOrFail(line[:-1])
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
                y = j.runGremlinQuery(query)
                for z in y: print '%s\t%s\t%s\t%s\t%s' % tuple(z)
            else:
                query += '.transform{ [funcName, "%s", funcLoc, it.signature] }' % (filename)
                y = j.runGremlinQuery(query)
                for z in y:
                    print '%s\t%s\t%s\t%s' % tuple(z)

if __name__ == '__main__':
    cli = CLI()
    cli.run()
