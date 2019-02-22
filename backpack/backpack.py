# Tucker Jaenicke
# HW3

import random

MAX_WEIGHT = 120
POP_SIZE = 50
GEN_LIMIT = 100
weights = [20,30,60,90,50,70,30]
values  = [	6, 5, 8, 7, 6, 9, 4]

# create random population of n candidates
# candidates are represented as a string of 7 0s and 1s
def init_pop(pop_size, chrom_size):
	pop = []
	for i in range(pop_size):
		candidate = []
		for j in range(chrom_size):
			# randomly create string of 0s and 1s
			candidate.append(random.randrange(2))
		pop.append(candidate)
	return pop

# returns the weight of the candidate
def get_weight(candidate):
	weight = 0
	# loop through chromsome
	for ind in range(len(candidate)):
		# if bit is 1, add the weight of that item to total
		if candidate[ind] > 0:
			weight += weights[ind]
	return weight

# returns the value of the candidate
def get_value(candidate):
	value = 0
	# loop through chromsome
	for ind in range(len(candidate)):
		# if bit is 1, add the value of that item to total
		if candidate[ind] > 0:
			value += values[ind]
	return value

# returns the fitness of the candidate
def fitness(candidate):
	# fitness is 0 if over max weight
	if get_weight(candidate) > MAX_WEIGHT:
		return 0
	# if unerweight, fitness is value
	else:
		return get_value(candidate)

# given two candidates, produces an offspring
# the offspring is a combination of its two parents
def reproduce(x, y):
	child = []
	# random number between 0 and length of chromosome
	c = random.randrange(len(x)+1)
	for i in range(len(x)):
		# add first half of parent x
		if i < c:
			child.append(x[i])
		# add second half of parent y
		else:
			child.append(y[i])
	return child

# given one candidate, randomly flips one bit
def mutate(child):
	ind = random.randrange(len(child))
	if child[ind] == 0:
		child[ind] = 1
	else:
		child[ind] = 0
	return child

# given a population, uses a genetic algorithm to find fittest individual
# return the fittest chromosome
def genetic_solve(pop):
	# runs for GEN_LIMIT generatiosn
	for i in range(GEN_LIMIT):
		# sort population
		pop.sort(reverse=True, key=fitness)
		# initialize new population array
		new_pop = []
		# creat POP_SIZE - 1 new children
		for i in range(POP_SIZE - 1):
			# choose two parents from top fal of population
			x = pop[random.randrange(POP_SIZE/2)]
			y = pop[random.randrange(POP_SIZE/2)]
			# create new child via reproductoin
			child  = reproduce(x, y)
			# mutates the child witha 1% probability
			if random.random() > 0.99:
				child = mutate(child)
			new_pop.append(child)
		# keep fittest of previous generation
		new_pop.append(pop[0])
		pop = new_pop
	return pop[0]

def print_pop(arr):
	for i in arr:
		print(i, end=" -- w: ")
		print(get_weight(i), end=", v: ")
		print(get_value(i), end=", fitness: ")
		print(fitness(i))

# create initial poulation
pop = init_pop(POP_SIZE, len(weights))
# solve
soln = genetic_solve(pop)
print(soln, " -- w:", get_weight(soln),", fitness:", fitness(soln))