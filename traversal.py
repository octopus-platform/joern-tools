#!/usr/bin/env python2

from joerntools.shelltool.LookupTool import LookupTool

DESCRIPTION = """Runs an arbitrary gremlin traversal."""

class Traversal(LookupTool):
    def __init__(self):
        LookupTool.__init__(self, DESCRIPTION)

    def _queryFromLine(self, line):
        return line
            
if __name__ == '__main__':
    tool = Traversal()
    tool.run()
