Gremlin.defineStep('forwardSlice', [Vertex, Pipe], { symbol ->
	_()
	.copySplit(
		_(),
		_().transform{
			it.sideEffect{first = true;}
			.outE('REACHES', 'CONTROLS')
			.filter{it.label == 'CONTROLS' || !first || it.var == symbol}
			.inV().gather{it}.scatter()
			.sideEffect{first = false}
			.loop(4){it.loops < 5}{true}
		}.scatter()
	).fairMerge()
	.dedup()
});

Gremlin.defineStep('backwardSlice', [Vertex, Pipe], { symbol ->
	_()
	.copySplit(
		_(),
		_().transform{
			it.sideEffect{first = true;}
			.inE('REACHES', 'CONTROLS')
			.filter{it.label == 'CONTROLS' || !first || it.var == symbol}
			.outV().gather{it}.scatter()
			.sideEffect{first = false}
			.loop(4){it.loops < 5}{true}
		}.scatter()
	).fairMerge()
	.dedup()
});
