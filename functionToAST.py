#!/usr/bin/env python2

from LookupTool import LookupTool

DESCRIPTION = """ Get the AST root of a function."""

class Func2AST(LookupTool):
    def __init__(self):
        LookupTool.__init__(self, DESCRIPTION)

    def _queryFromLine(self, line):
        query = """ g.v(%s).functionToAST()""" % (line)
        return query

if __name__ == '__main__':
    tool = Func2AST()
    tool.run()
