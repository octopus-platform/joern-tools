
from octopus.server.DBInterface import DBInterface
from octopus.shelltool.PipeTool import PipeTool


class JoernTool(PipeTool):
    
    def __init__(self, DESCRIPTION):
        PipeTool.__init__(self, DESCRIPTION)
        self.dbName = None

    def setDBName(self, dbName):
        self.dbName = dbName

    # @Override
    def streamStart(self):
        self.dbInterface = DBInterface()
        self.dbInterface.connectToDatabase(self.dbName)
    
    def _runGremlinQuery(self, query):
        return self.dbInterface.runGremlinQuery(query)
    
