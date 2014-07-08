#!/usr/bin/env python2

import sys
from joerntools.shelltool.LookupTool import LookupTool

DESCRIPTION = """Lookup the location of a node in the code."""

class Location(LookupTool):
    
    def __init__(self):
        LookupTool.__init__(self, DESCRIPTION)
        
     # @Override
    def processLine(self, line):
 
        # Note, that since we override processLine,
        # queryFromLine will not be called either.

        # For functions, get location of function
        # For statement, get location of statement
        # For AST nodes, get location of statement
        # For Symbols, get location of function
        
        id = line
        query = """g.v(%s)
        .ifThenElse{it.type == 'Function'}{
         it.sideEffect{loc = it.location; }.functionToFile()
         .sideEffect{filename = it.filepath; }
         }{
           it.ifThenElse{it.type == 'Symbol'}
           {
             it.transform{ g.v(it.functionId) }.sideEffect{loc = it.location; }
             .functionToFile()
             .sideEffect{filename = it.filepath; }
            }{
             it.ifThenElse{it.isCFGNode == 'True'}{
               it.sideEffect{loc = it.location}
               .functions().functionToFile()
               .sideEffect{filename = it.filepath; }
             }{
              // AST node
              it.statements().sideEffect{loc = it.location; }
              .functions()
              .functionToFile().sideEffect{filename = it.filepath; }
              }
           }
        }.transform{ filename + ':' + loc }
        
        """ % (id)

        y = self.j.runGremlinQuery(query)
        for x in y:
            print x
        

if __name__ == '__main__':
    tool= Location()
    tool.run()
