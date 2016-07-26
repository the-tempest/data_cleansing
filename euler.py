def list_of_primes(mina, maxa):
	a = []
	for x in range(mina, maxa):
		if isaPrime(x):
			a.append(x)

	return a

def solve27():
	
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

def isaPrimeList(number, list_of_primes):
	if number <0 or number == 1:
		return False

	for item in list_of_primes:
		if number % item == 0:
			return False
	return True


def solve9():

	for a in range(334):
		for b in range(1001-a):
			if b == a:
				continue
			c = 1000 - a - b

			if c == b:
				continue

			if (a*a + b*b) == c * c : 
				return a,b,c

			else:
				continue

def solve10(max_num):
	total = 0
	prime_list = [2]
	for x in range(3,max_num+1,2):
		if isaPrimeList(x, prime_list) == True:
			print x
			total += x
			prime_list.append(x)
			#print prime_list
	return total

