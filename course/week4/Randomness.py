import random
import numpy as np

random.seed(1234)

print(random.random())
print(random.uniform(25,50))

#Uniform
unifNumbers = [random.uniform(0,1) for _ in range(1000)]
print(unifNumbers)

#Normal
mu = 0
sigma = 1
print(random.normalvariate(mu, sigma))

mu = 0
sigma = 1
[random.normalvariate(mu, sigma) for _ in range(10000)]

'''
Random Sampling from a Population
From lecture, we know that Simple Random Sampling (SRS) has the following properties:

Start with known list of N* population units, and randomly select *n units from the list
Every unit has equal probability of selection = n/N
All possible samples of size n are equaly likely
Estimates of means, proportions, and totals based on SRS are UNBIASED (meaning they are equal to the population values 
on average)
'''

mu = 0
sigma = 1
Population = [random.normalvariate(mu, sigma) for _ in range(10000)]

SampleA = random.sample(Population, 500)
SampleB = random.sample(Population, 500)

np.mean(SampleA)
np.std(SampleA)
np.mean(SampleB)
np.std(SampleB)

means = [np.mean(random.sample(Population, 1000)) for _ in range(100)]
np.mean(means)