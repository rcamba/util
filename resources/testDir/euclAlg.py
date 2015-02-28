#find gcd, euclidean algorithm
def eucAlg(x,y):
	numToDivide=x

	divisor=y
	ans=-1
	prevAns=-1
	while ans>0 or ans <0:
		prevAns=ans
		ans=numToDivide%divisor
		numToDivide=divisor
		divisor=ans
		
	print prevAns

for i in range(1,18):
	eucAlg(18,i)