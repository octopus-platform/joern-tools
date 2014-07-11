
"""
A shell tool that constructs queries from arguments and flags and
outputs results. In contrast to StartTool, this tool performs chunking
to increase performance.
"""

from joerntools.DBInterface import DBInterface
from joerntools.shelltool.CmdLineTool import CmdLineTool

CHUNK_SIZE = 256

class ChunkStartTool(CmdLineTool):

    def __init__(self, DESCRIPTION):
        CmdLineTool.__init__(self, DESCRIPTION)

    # @Override
    def _constructIdQuery(self):
        pass

    # @Override
    def _constructQueryForChunk(self, chunk):
        pass

    # @Override
    def handleChunkResult(self, res, chunk):
        pass

    def _runImpl(self):
        
        self.dbInterface = DBInterface()
        self.dbInterface.connectToDatabase()

        query = self._constructIdQuery()
        ids = self.dbInterface.runGremlinQuery(query)
        
        for chunk in self.dbInterface.chunks(ids, CHUNK_SIZE):
            query = self._constructQueryForChunk(chunk)
            res = self.dbInterface.runGremlinQuery(query)
            self._handleChunkResult(res, chunk)

    
