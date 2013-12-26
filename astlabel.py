
DESCRIPTION = """Labels AST nodes according to a labeling scheme. """

from joerntools.shelltool.GraphvizTool import GraphvizTool

class ASTLabel(GraphvizTool):
    
    def __init__(self):
        GraphvizTool.__init__(self, DESCRIPTION)
        
    # @Override
    def processGraph(self, G):
        for node in G: self.processNode(G, node)
        print G

    def processNode(self, G, node):
        attributes = str(node.attr['label']).split('\n')
        attrDict = {}
        for a in attributes:
            i = a.find(':')
            print i
            k = a[:i]
            v = a[i+1:]
            print k,v 
            attrDict[k] = v
        
        children = G.out_edges([node])
        
        if len(children) == 0:
            node.attr['label'] = attrDict['code']
        else:
            node.attr['label'] = attrDict['type']
        
if __name__ == '__main__':
    tool = ASTLabel()
    tool.run()
