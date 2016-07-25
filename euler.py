def list_of_primes(mina, maxa):
	a = []
	for x in range(mina, maxa):
		if isaPrime(x):
			a.append(x)

	return a

def solve():
	
	max_n = 0
	b_range = list_of_primes(-999,1000)

	for a in range(-999, 1000): #a
		print a
		for b in b_range: #b
			

			if (b % 2) == 1:
				if (a % 2) != 1:
					continue
			else:
				if (a % 2) != 0:
					continue

			n = 0
			result = n*n + a*n + b 
			
			while isaPrime(result) == True:
				
				n +=1
				#print n
				result = n*n + a*n + b
			
			if n > max_n:
				max_n = n
				returner = max_n, a, b
			n = 0
			
	return returner[1]*returner[2]
	
def isaPrime(number):
	if number < 0:
		return False

	for x in range(2,number/2):
		if (number % x) == 0:
			return False
	return True