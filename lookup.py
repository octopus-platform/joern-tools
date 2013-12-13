#!/usr/bin/env python2

from ParseLocationString import parseLocationOrFail
from PipeTool import PipeTool
from joern.all import JoernSteps

DESCRIPTION = """Lookup AST nodes by type and name"""

class Lookup(PipeTool):
    def __init__(self):
        PipeTool.__init__(self, DESCRIPTION)
    
    # @Override
    def streamStart(self):
        self.j = JoernSteps()
        self.j.connectToDatabase()

    # @Override
    def processLine(self, line):
        (nodeType, code) = line.split('\t')
        
        query = """queryNodeIndex('type:%s AND code:"%s"')""" % (nodeType, code)
        query += """
        .astNodeToFunction().sideEffect{ loc = it.location; name = it.functionName}
        .functionToFile().sideEffect{filename = it.filepath}
        .transform{[name, filename, loc]}
        """

        y = self.j.runGremlinQuery(query)
        for x in y:
            print '%s\t%s:%s' % tuple(x)

if __name__ == '__main__':
    tool = Lookup()
    tool.run()
