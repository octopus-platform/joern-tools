#!/usr/bin/env python2

from DemuxTool import DemuxTool
from csvAST.CSVToPythonAST import pythonASTFromCSV
from csvAST.ASTPrinter import ASTPrinter
import pickle

DESCRIPTION = """Extracts string features from ASTs given in CSV
format or as pickle'd ASTs."""

class AST2Features(DemuxTool):
    def __init__(self):
        DemuxTool.__init__(self, DESCRIPTION)

    # @Override
    def processLines(self):
        ast = pythonASTFromCSV(self.lines)
        printer = ASTPrinter()
        printer.processTree(ast)
        for l in printer.getOutput():
            self.output(l + '\n')

if __name__ == '__main__':
    tool = AST2Features()
    tool.run()
