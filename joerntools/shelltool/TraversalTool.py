
from PipeTool import PipeTool
from joern.all import JoernSteps

class TraversalTool(PipeTool):
    
    def __init__(self, DESCRIPTION):
        PipeTool.__init__(self, DESCRIPTION)

    # @Override
    def streamStart(self):
        self.j = JoernSteps()
        self.j.connectToDatabase()
    
    # @Override
    def processLine(self, line):
        query = self.queryFromLine(line)

        y = self.j.runGremlinQuery(query)
        self.outputResult(y)

    def queryFromLine(self, line):
        return line
    
    def outputResult(self, result):
        
        if type(result) == type([]):
            for r in result:
                self.output(str(r) + '\n')
        else:
            self.output(str(result) + '\n')
