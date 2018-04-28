# cde abc    cdeee abcc    jackoo jacc    abcdk cdefgc
x = "cdee".lower()
y = "abcc".lower()
ofXinY1 = ""
ofYinX = ""
if len(x) < len(y):
	for i in x:
		if i in y:
			ofXinY1 += i
	print(len(y) - len(ofXinY1))
	print(len(ofXinY1))
	print(ofXinY1)
if len(x) > len(y):
	for i in y:
		if i in x:
			ofXinY1 += i
	for o in x:
		if o in y:
			ofYinX += o
	if len(ofXinY1) < len(ofYinX):
		pass
	print(len(ofXinY1))
	print(ofXinY1, ofYinX)
if len(x) == len(y):
	for i in x:
		if i in y:
			ofXinY1 += i
	for o in y:
		if o in x:
			ofXinY1 += i
	print(len(ofXinY1))
	print(ofXinY1)
"""
sasadadasd
"""
