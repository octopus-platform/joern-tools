/**
   Hooked to return only visible nodes.
*/

Object.metaClass.queryNodeIndex = { query, honorVisibility = true ->
        index = g.getRawGraph().index().forNodes(NODE_INDEX)
	if(honorVisibility)
		new Neo4jVertexSequence(index.query(query), g)._().visible()
	else
		new Neo4jVertexSequence(index.query(query), g)._()
}

