echo 'type:Symbol AND code:memcpy' | ./lookup.py --attributes functionId | head -n 10 | awk '{split($2,a,":"); print a[2]}' | ./ast.py | ./astlabel.py | ./ast2features.py | ./demux.py
