
Gremlin.defineStep('functionToAPISymbolNodes', [Vertex, Pipe], {
        _() // Function node
        .functionToASTNodes()
        .filter{it.type == 'IdentifierDeclType' || it.type == 'ParameterType' || it.type == 'Callee' || it.type == 'Sizeof'}
});

