#!/usr/bin/env python2

from DemuxTool import DemuxTool
from csvAST.CSVToPythonAST import pythonASTFromCSV
from csvAST.PythonASTToPrunedAST import PythonASTToPrunedAST
from csvAST.ParseTreeFilter import ParseTreeFilter
from csvAST.ASTPrinter import ASTPrinter
import pickle

DESCRIPTION = """Extracts string features from ASTs given in CSV
format or as pickle'd ASTs."""

class AST2Features(DemuxTool):
    def __init__(self):
        DemuxTool.__init__(self, DESCRIPTION)
        self.pruning = PythonASTToPrunedAST()

        self.argParser.add_argument('-n', '--nodes-of-interest',
                                    nargs='+', type = str,
                                    help="""Type of nodes of
                                    interest""", default = [])
        
        self.argParser.add_argument('-d', '--discard', action='store_true',
                                    help = """Discard nodes of
                                    interest instead of preserving
                                    them.""", default = False)

    # @Override
    def processLines(self):
        ast = pythonASTFromCSV(self.lines)
        
        if self.args.nodes_of_interest != []:
            self.pruning.nodeTypesOfInterest = self.args.nodes_of_interest
            self.pruning.keepNodesOfInterest = (not self.args.discard)
            self.pruning.processTree(ast)
            ast = self.pruning.getPrunedTree()
        
        printer = ASTPrinter()
        printer.processTree(ast)
        
        for l in printer.getOutput():
            self.output(l + '\n')

if __name__ == '__main__':
    tool = AST2Features()
    tool.run()
