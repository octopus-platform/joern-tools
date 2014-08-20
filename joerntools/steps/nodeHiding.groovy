
/**
	Return only visible nodes.
*/

Gremlin.defineStep('visible', [Vertex, Pipe], {
	_().filter{
		if(it.type == 'File')
			(it.hidden != '1')
		else if(it.type == 'Function')
			it.functionToFiles().hidden.toList()[0] != '1'
		else if( (l = it.functions().functionToFiles().hidden.toList() ) != [])
			l[0] != '1'
		else
			true
	}
});

