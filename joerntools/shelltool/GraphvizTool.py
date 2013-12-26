
from joerntools.shelltool.PipeTool import PipeTool
from pygraphviz import AGraph

class GraphvizTool(PipeTool):
    
    def __init__(self, description):
        PipeTool.__init__(self, description)
        self.lines = []

    def processLine(self, line):
        ENDMARKER = '###'
        
        if line == ENDMARKER:
            self.processLines()
            self.lines = []
        else:
            self.lines.append(line)
            
    def processLines(self):
        s = ''.join(self.lines)
        G = AGraph(string=s)


if __name__ == '__main__':
    tool = GraphvizTool('foo')
    tool.run()

