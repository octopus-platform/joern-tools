#!/usr/bin/env python2

import sys
from LookupTool import LookupTool

DESCRIPTION = """List contents of function with given id."""

class Function(LookupTool):
    
    def __init__(self):
        LookupTool.__init__(self, DESCRIPTION)
        
    def _queryFromLine(self, line):
        
        id = line
        query = """g.v(%s).astNodeToFunction()
        """ % (id) 
        return query
            

if __name__ == '__main__':
    tool= Function()
    tool.run()
