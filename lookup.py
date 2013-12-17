#!/usr/bin/env python2

from ParseLocationString import parseLocationOrFail
from PipeTool import PipeTool
from joern.all import JoernSteps

DESCRIPTION = """Lookup nodes using lucene queries and output one row
for each property each matching node. Rows are in the format '[nodeId,
attributeName, attributeValue]'.
"""

class Lookup(PipeTool):
    def __init__(self):
        PipeTool.__init__(self, DESCRIPTION)

    # @Override
    def streamStart(self):
        self.j = JoernSteps()
        self.j.connectToDatabase()

    # @Override
    def processLine(self, line):
        query = line
        if query.startswith('id:'):
            id = query.split(':')[1]
            query = 'g.v(%s).transform{ [it.id, it] }' % (id)
        else:
            query = """queryNodeIndex('%s').transform{ [it.id, it]}""" % (query)
        
        y = self.j.runGremlinQuery(query)
        for x in y:
            self._outputRecord(x)
            
    def _outputRecord(self, record):
        id, node = record
        keys = [k for k in node]
        keys.sort()
        keyValPairs = [str(k) + ':' + str(node[k]) for k in keys]
        self.output('id:%s\t%s\n' % (id, '\t'.join(keyValPairs)) )

if __name__ == '__main__':
    tool = Lookup()
    tool.run()
