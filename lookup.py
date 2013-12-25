#!/usr/bin/env python2

from LookupTool import LookupTool

DESCRIPTION = """Lookup nodes using lucene queries and output one row
for each matching node. Rows are in the format functionId TAB
attributeKey:attributeValue TAB ...'
"""

class Lookup(LookupTool):
    def __init__(self):
        LookupTool.__init__(self, DESCRIPTION)

    def _queryFromLine(self, line):
        
        luceneQuery = line
        if luceneQuery.startswith('id:'):
            id = luceneQuery.split(':')[1]
            query = 'g.v(%s)' % (id)
        else:
            query = """queryNodeIndex('%s')""" % (luceneQuery)
        
        return query
            
if __name__ == '__main__':
    tool = Lookup()
    tool.run()
