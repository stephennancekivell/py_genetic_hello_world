#!/usr/bin/env python

import Levenshtein
import random
import string

TARGET = "Hello world!"
POP_SIZE = 500
GENERATIONS = 200

def fitness(phrase):
    #lower is better.
    return Levenshtein.distance(TARGET,phrase)

def genRandomPhrase():
    #return a new random phrase of varying length
    p = []
    for i in range(0, random.randint((len(TARGET)/3)*2, (len(TARGET)/3)*4)):
        p.append(random.choice(string.printable))

    p = ''.join(p)
    return (fitness(p),p)

def mutate(phrase):
    #on this chance add some more characters in random locations.
    add = random.randint(-3,3)
    if add > 0:
        for a in range(add):
            c = random.choice(string.printable)
            i = random.randint(0,len(phrase)-1)
            phrase = phrase[:i] + c + phrase[i:]

    # on this chance delete random characters
    delete = random.randint(-3,3)
    if delete > 0:
        for d in range(delete):
            i = random.randint(0,len(phrase)-1)
            phrase = phrase[:i]+phrase[i+1:]

    return phrase

def mate(mother,father):
    #merge the two phrases with random choice
    child = []
    i=0
    while i < len(mother) and i < len(father):
        child.append(random.choice([mother[i],father[i]]))
        i+=1
    #either the mother or the father could be longer.
    while i < len(mother):
        if random.choice([True,False]):
            child.append(mother[i])
        i+=1
    while i < len(father):
        if random.choice([True,False]):
            child.append(father[i])
        i+=1
    child = ''.join(child)
    if random.randint(0,100) < 20:
        child = mutate(child)
    return (fitness(child), child)

# population as a sorted list [(fitness,phrase),..]
population = []
for i in range(POP_SIZE):
    population.append(genRandomPhrase())

population.sort()

for g in range(GENERATIONS):
    p2 = population[:(POP_SIZE/100)*20] # keep the top 20%

    #mate the rest with a tornament
    for i in range(len(population)-len(p2)):
        f1 = random.choice(population)
        f2 = random.choice(population)

        m1 = random.choice(population)
        m2 = random.choice(population)

        if f1[0] < f2[0]: f =f1[1]
        else: f = f2[1]

        if m1[0] < m2[0]: m =m1[1]
        else: m = m2[1]

        p2.append(mate(f,m))

    p2.sort()
    population = p2
    print g,population[0][0],population[0][1]
