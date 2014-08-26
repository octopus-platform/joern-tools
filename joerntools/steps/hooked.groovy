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

Object.metaClass.getFilesByName = { filename, honorVisibility = true ->
	query = "$NODE_TYPE:$TYPE_FILE AND $NODE_FILEPATH:$filename"
	queryNodeIndex(query, honorVisibility)
}

Object.metaClass.getFunctionsByName = { name, honorVisibility = true ->
	getNodesWithTypeAndName(TYPE_FUNCTION, name, honorVisibility)
}

Object.metaClass.getNodesWithTypeAndName = { type, name, honorVisibility = true  ->
	query = "$NODE_TYPE:$type AND $NODE_NAME:$name"
	queryNodeIndex(query, honorVisibility)
}

Object.metaClass.getFunctionsByFileAndName = { filename, name, honorVisibility = true ->
	getFunctionsByFilename(filename, honorVisibility)
	.filter{ it.name == name }
}

Object.metaClass.getFunctionsByFilename = { name, honorVisibility = true ->
	query = "$NODE_TYPE:$TYPE_FILE AND $NODE_FILEPATH:$name"
	queryNodeIndex(query, honorVisibility)
	.out('IS_FILE_OF')
	.filter{ it.type == TYPE_FUNCTION }
}
