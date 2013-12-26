
from PipeTool import PipeTool
from joern.all import JoernSteps

class JoernTool(PipeTool):
    
    def __init__(self, DESCRIPTION):
        PipeTool.__init__(self, DESCRIPTION)
    
     # @Override
    def streamStart(self):
        self._connectToDatabase()
    
    def _connectToDatabase(self):
        self.j = JoernSteps()
        self.j.connectToDatabase()
    
    def _runGremlinQuery(self, query):
        return self.j.runGremlinQuery(query)
    
