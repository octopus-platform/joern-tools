
Gremlin.defineStep('functionToAPISymbolNodes', [Vertex, Pipe], {
        _() // Function node
        .functionToASTNodes()
        .filter{it.type == 'IdentifierDeclType' || it.type == 'ParameterType' || it.type == 'Callee' || it.type == 'Sizeof'}
});


Object.metaClass.edgesInX = { X -> 
	X._().transform{ g.v(it) }
	.outE()
	.filter{
		p = it.inV().id.toList()[0]
		X.contains(p)
	}.id
}
