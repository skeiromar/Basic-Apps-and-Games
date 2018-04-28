
def buildMap(s):
	theMap = {}
	for char in s:
		if char not in theMap:
			theMap[char] = 1
		else:
			theMap[char] += 1
	return theMap

print(buildMap("hellobitch"))

