

def countOdds(list):
	odds=[]
	asd=0
	l=list
	for z in l:
		
		oddCount=0
		for q in z:
			if (int(q) %2) !=0:
				oddCount+=1
				
		if(oddCount==6):
			
			asd+=1
				
				
		
	print asd
	return asd

r=["0","1","2","3","4","5","6","7","8","9"]

s=""
l=[]


for a in r:
	
	for b in r:
	
		for c in r:
		
			for d in r:
			
				for e in r:
					
					for f in r:
						l.append( str(a) + str(b) + str(c) + str(d) + str(e) + str(f) )



	
	
"""
evenCount=0
for z in l:
	
	
	for q in z:
		if (int(q) %2) ==0:
			evenCount+=1
			break
			
	
			
			
	
print evenCount
"""
"""
fb=0
forback=[]
for z in l:
	
	
	q=z
		
		
	if q[0]==q[5] and q[1]==q[4] and q[2]==q[3]:
		fb+=1
		forback.append(z)
		print z
		

		
print fb
"""

"""
lc=[]
count=0
for z in l:
	if "1" in z and "2" in z and "3" in z:
		temp=z.replace("1","",1).replace("2","",1).replace("3","",1)
		
		
		if "1" in temp and "2" in temp and "3" in temp:
			count+=1
			lc.append(z)

print lc
print count
"""

import math
from sys import argv
def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

if __name__ == '__main__':
	try:
		
		print nCr(int(argv[1]),int(argv[2]))
	except IOError:
		print "missing args"