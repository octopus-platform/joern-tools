from joerntools.shelltool.TraversalTool import TraversalTool
from py2neo import neo4j

DEFAULT_TAGNAME = 'tag'
BATCH_SIZE = 1000


class JoernTag(TraversalTool):
    
    def __init__(self, DESCRIPTION):
        TraversalTool.__init__(self, DESCRIPTION)
        
        self.argParser.add_argument("-t", "--tag", default = DEFAULT_TAGNAME)
        
        self.inputPairs = []

    def processLine(self, line):
        # [nodeId, tagValue]
        X = line.split('\t')
        X = [int(X[0]), X[1]]
         
        self.inputPairs.append(X)
         
        if len(self.inputPairs) == BATCH_SIZE:
            self.processBatch(self.inputPairs)
            self.inputPairs = []

    # @Override
    def processBatch(self, pairs):
        
        batch = neo4j.WriteBatch(self.dbInterface.j.graphDb)
        graphDbURL = self.dbInterface.j.getGraphDbURL()
        if graphDbURL[-1] == '/': graphDbURL = graphDbURL[:-1]

        for (nodeId, tagVal) in pairs:
                    
            nodeURL = graphDbURL + '/node/' + str(nodeId)
            node = neo4j.Node(nodeURL)
            batch.set_property(node, self.args.tag , tagVal)
        
        batch.submit()
        
    def streamEnd(self):

        if len(self.inputPairs) != 0:
            self.processBatch(self.inputPairs)
        