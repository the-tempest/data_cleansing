import math



def list_of_primes(mina, maxa):
	a = []
	for x in range(mina, maxa):
		if isaPrime(x):
			a.append(x)
	return a


def solve4():
	prime_list = gen_primes_sieve(998002)
	lst = []
	for x in range(998001,10000,-1):
		#print x
		if prime_list[x] == True:
			continue
		elif str(x) == str(x)[::-1]:
			lst.append(x)

	for item in lst:
		factors = return_factors(item)
		for x in range(0,len(factors), 2):
			if (factors[x]>=100 and factors[x]<=999) and (factors[x+1]>=100 and factors[x+1]<=999):
				return item, factors[x], factors[x+1]

	return "fail"


def return_factors(num):
	lst = []
	for x in range(1,num/2):
		if x in lst:
			break
		if num % x == 0:
			val = num/x
			lst.append(x)
			if x == val:
				continue 
			lst.append(val)

	return lst 



def solve8():
	start = time.time()
	num = "7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450"
	big_prod = string_num_prod(num[0:13])
	#print big_prod
	for x in range(1, len(num) - 13): # subtract 13 because problem asks for 13 size clumps of the number
		cur_string = num[x:x+13]
		if "0" in cur_string:
			continue

		cur_prod = string_num_prod(num[x:x+13])
		if cur_prod > big_prod:
			big_prod = cur_prod

	print time.time() - start
	return big_prod

def string_num_prod(string):
	total = 1
	for x in range(len(string)):
		total *= int(string[x])
	return total

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

def gen_triangle_list(max_index):
	total = 0
	lst = []
	for x in range(max_index):
		total += x
		lst.append(total)

	return lst

def solve12():
	return 0


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


def solve21():
	lst = []
	for x in range(1,10000):
		factors1 = return_factors(x)

		if x in factors1:
			factors1.remove(x)

		d_a = sum(factors1)

		factors2 = return_factors(d_a)
		
		if d_a in factors2:
			factors2.remove(d_a)

		d_b = sum(factors2)

		#print d_b, x

		if (d_b == x) and (x != d_a) :
			if x not in lst:
				lst.append(x)
			if d_a not in lst:
				lst.append(d_a)

	return sum(lst)




from itertools import permutations

def solve24():
	a = '0123456789'
	perms = [''.join(x) for x in permutations(a)]
	perms.sort
	return perms[999999]


def solve25():

	max_index = 10000
	min_index = 0
	x = 5000
	
	while True:
		print x
		curr_num = gen_fib_list(x)[x]
		if number_digits(curr_num) == 1000:
			x = find_first_1000(x)
			return x

		elif(number_digits(curr_num) > 1000):
			max_index = x
			x = x - (x - min_index)/2

		else:
			min_index = x
			x = x + (max_index - min_index)/2

def find_first_1000(x):

	while (number_digits(gen_fib_list(x)[x]) == 1000):
		x -= 1

	return x+1



def gen_fib_list(max_index):
	fibs = [0,1,1]
	for x in range(3,max_index+1):
		fibs.append(fibs[x-1] + fibs[x-2])
	return fibs

def number_digits(num):
	return len(str(num))


letter_number_count = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
"ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]

single_digits = "onetwothreefourfivesixseveneightnine"

tens = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety" ]
other_tens = "twentythirtyfourtyfiftysixtyseventyeightyninety"

hundred = "hundred"
ands = "and"
one_thousand = "onethousand"

def solve17():
	sums = 0
	number_len_list = []
	for item in letter_number_count:
		sums += len(item)
		number_len_list.append(len(item))


	for item in tens:
		sums += len(item)* 10
		sums += len(single_digits)

	first_100 = sums

	for x in range(0,9):
		sums += (len(letter_number_count[x]) + len(hundred)) * 100
		sums += len(ands) * 99
		sums += first_100

	sums += len(one_thousand)

	return sums
import time

def solve28():
	start = time.clock()
	square_start = 3
	sub_tract = 2
	sums = 1
	while square_start <= 10001:
		a = square_start**2
		for x in range(4):
			sums +=  a - x*sub_tract
		sub_tract += 2
		square_start +=2
	end = time.clock()

	print end-start
	return sums

import collections

def solve32():
	lst10 = []
	lst100 = []
	lst1000 = []
	pandigital = []
	for x in range(10,99):
		if (x%10 != 0) and (x%11 != 0 ):
			lst10.append(x)

	for x in range(100,999):
		num = str(x)
		if ("0" not in num):
			results = collections.Counter(num)
			values = results.values()
			if (2 not in values) and (3 not in values):
				lst100.append(x)

	#return lst100

	for i in lst10:
		for j in lst100:
			i_str = str(i)
			j_str = str(j)
			tot_string = i_str + j_str

			results = collections.Counter(tot_string)
			values = results.values()
			if max(values) > 1: # means that some value occurs 2 or more times
				continue


			x = i*j
			tot_string = str(x) + tot_string

			results = collections.Counter(tot_string)
			values = results.values()
			if (max(values) > 1) or ("0" in tot_string): # means that some value occurs 2 or more times
				continue
			
			else:
				print i,j,x
				if (x not in pandigital):
					pandigital.append(x)



	for x in range(1000,9999):
		num = str(x)
		if ("0" not in num):
			results = collections.Counter(num)
			values = results.values()
			if max(values) == 1:
				lst1000.append(x)

	for i in range(1,10):
		for j in lst1000:
			i_str = str(i)
			j_str = str(j)
			tot_string = i_str + j_str

			results = collections.Counter(tot_string)
			values = results.values()
			if max(values) > 1: # means that some value occurs 2 or more times
				continue


			x = i*j
			tot_string = str(x) + tot_string

			results = collections.Counter(tot_string)
			values = results.values()
			if (max(values) > 1) or ("0" in tot_string): # means that some value occurs 2 or more times
				continue
			
			else:
				print i,j,x
				if (x not in pandigital):
					pandigital.append(x)


	#return lst1000
	return pandigital

import itertools

def solve35():
	big_sieve = gen_primes_sieve(1000000)
	lst = []
	primes = []

	for x in range(len(big_sieve)):
		if big_sieve[x] == True:
			primes.append(x)

	#print primes

	for item in primes:
		#print item
		if item in lst:
			continue

		a = str(item)
		if (item != 2) and ("2" in a) or ("4" in a) or ("6" in a) or ("8" in a) or ("0" in a): 
			continue 

		perms = [item]
		rotator = item
		count = 0
		while count < len(a):
			rotator = rotate1(rotator)
			perms.append(rotator)
			count += 1

		total = 0
		for x in range(len(perms)): # item is a string

			if big_sieve[perms[x]] == False:
				break
			else:
				total += 1

		print total, len(perms)

		if total == len(perms):
			print "here"
			for item2 in perms:
				if item2 not in lst:
					lst.append(item2)
			print lst


	return lst

def rotate1(x):

	num = str(x)

	first = num[0]

	num = num[1:]
	num += first

	return int(num)


def solve36():
	sums = 0

	for x in range(10000000):
		num = str(x)
		rev_num = num[::-1]

		base_hex = hex(x)
		base_hex = base_hex[2:]

		rev_hex = base_hex[::-1]

		if rev_hex != base_hex:
			continue

		

		if num != rev_num:
			continue


		

		binary = bin(x)

		#strip 0b from it
		binary = binary[2:]

		rev_binary = binary[::-1]

		if binary == rev_binary:
			print x
			sums += x

	return sums
		