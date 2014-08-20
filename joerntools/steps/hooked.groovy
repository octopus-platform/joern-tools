/**
   Hooked to return only visible nodes.
*/

Object.metaClass.queryNodeIndex = { query ->
        index = g.getRawGraph().index().forNodes(NODE_INDEX)
	new Neo4jVertexSequence(index.query(query), g)._().visible()
}
