import math

def list_of_primes(mina, maxa):
	a = []
	for x in range(mina, maxa):
		if isaPrime(x):
			a.append(x)


	return a

def solve7():
	x = 110000
	upper = x
	lower = 100000
	while True:
		print x
		if sum(gen_primes_sieve(x)) == 10001:
			return x
		elif sum(gen_primes_sieve(x)) > 10001:
			upper = x
			x = x - ((x-lower)/2)

		else:
			lower = x
			x = x + ((upper-x)/2)

		






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
	sieve = gen_primes_sieve(max_num)
	return find_sum(sieve)


def gen_primes_sieve(num):
	''' generates all primes up to a num via the sieve of erathsoajfkldjf;lajdfl'''
	sieve = [True] * (num)
	sieve[0] = False
	sieve[1] = False

	for i in range(2,int((num**0.5))):
		if sieve[i] == True: 
			a = i*i
			while a < num:
				sieve[a] = False
				a += i
	return sieve

def find_sum(sieve):
	total= 0 
	for x in range(len(sieve)):
		if sieve[x] == True:
			total += x
		
	return total

def gen_next_collatz(num):
	if (num % 2 == 0):
		return num / 2
	else:
		return 3*num + 1

def gen_collatz_sequence(start,c_dict):
	sequence = []
	curr_num = start
	
	#print "here"
	while True:
		sequence.append(curr_num)

		if curr_num in c_dict:
			#print "skip!"
			#sequence.append(1)
			break
		if curr_num == 1:
			# if len(sequence) > 1:
			# 	sequence.append(1)
			break

		curr_num = gen_next_collatz(curr_num)
		#sequence.append(curr_num)

		

	for x in range(len(sequence)):
		if sequence[x] in c_dict:
			break

		else:
			c_dict[sequence[x]] = len(sequence[x+1:]) + c_dict[curr_num]
	#sequence.append(1)
	return sequence, c_dict #because it will skip 1 actually	

import time


def solve14():
	# all number in the collatz_dictionary are keyed right just the values seem to be off by 1
	start = time.time()
	collatz_dict = {1:0}
	max_len = 0
	max_index = 0
	for x in range(1,1000000):
		#print x
		if x in collatz_dict:
			#print x
			#print "skip!"
			continue
		else:
			a,b = gen_collatz_sequence(x, collatz_dict)




	v = list(collatz_dict.values())
	k = list(collatz_dict.keys())
	#print collatz_dict

	elasped = time.time() - start
	print elasped
	print collatz_dict
	return k[v.index(max(v))] 