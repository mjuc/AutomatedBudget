from random import random,uniform,randrange

from numpy import floor


MUTATION_RATE = 1
MUTATION_REPEAT_COUNT = 2
CROSSOVER_RATE = 70
THRESHOLD = 1000
USABLE_AMOUNT = 0

class Genome():
    def __init__(self,chromosomes,fitness):
        self.chromosomes=chromosomes
        self.fitness=fitness

def evaluate(chromosomes,conditions):
    spentAmount = 0
    for i in range(len(chromosomes)):
        if conditions[i]["isPercentage"]:
            spentAmount += conditions[i]["value"] * USABLE_AMOUNT * chromosomes[i] / 100
        else:
            spentAmount += conditions[i]["value"] * chromosomes[i]
    return USABLE_AMOUNT - spentAmount

def createNewPopulation(size,conditions):
    population = []
    print("Conditions given to create new pop: ",conditions)
    for i in range(size):
        chromosomes = []
        for condition in conditions:
            if condition["isExtendable"]:
                chromosomes.append(uniform(0,5))
            else:
                chromosomes.append(random())
        fitness = evaluate(chromosomes,conditions)
        newGenome = Genome(chromosomes,fitness)
        population.append(newGenome)
    return population

def findBestGenome(population):
    allFitness = [i.fitness for i in population]
    bestFitness = min(allFitness)
    return population[allFitness.index(bestFitness)]

def tournamentSelection(population,k):
    selected = [population[randrange(0, len(population))] for i in range(k)]
    bestGenome = findBestGenome(selected)
    return bestGenome

def swapMutation(chromo):
    for x in range(MUTATION_REPEAT_COUNT):
        p1, p2 = [randrange(1, len(chromo) - 1) for i in range(2)]
        while p1 == p2:
            p2 = randrange(1, len(chromo) - 1)
        log = chromo[p1]
        chromo[p1] = chromo[p2]
        chromo[p2] = log
    return chromo

def copyChromosomes(parent1,parent2,conditions):
    size = len(parent1)
    child = [-1] * size
    
    for i in range(size):
        if randrange(0,1)==0:
            child[i]=parent1[i]
        else:
            child[i]=parent2[i]
    
    if randrange(0, 100) < MUTATION_RATE:
        pass
        child = swapMutation(child)
    
    newGenome = Genome(child,evaluate(child,conditions))
    return newGenome

def orderOneCrossover(parent1, parent2):
    size = len(parent1)
    child = [-1] * size

    point = randrange(1, size - 4)

    for i in range(point, point + 4):
        child[i] = parent1[i]
    point += 4
    point2 = point
    while child[point] in [-1, 0]:
        if child[point] != 0:
            if parent2[point2] not in child:
                child[point] = parent2[point2]
                point += 1
                if point == size:
                    point = 0
            else:
                point2 += 1
                if point2 == size:
                    point2 = 0
        else:
            point += 1
            if point == size:
                point = 0

def reproduction(population,conditions):
    parent1 = tournamentSelection(population, 10).chromosomes
    parent2 = tournamentSelection(population, 6).chromosomes
    while parent1 == parent2:
        parent2 = tournamentSelection(population, 6).chromosomes
    
    if randrange(0, 100)<CROSSOVER_RATE and len(parent1) > 2:
        return orderOneCrossover(parent1, parent2)
    else:
        return copyChromosomes(parent1,parent2,conditions)

def parseValue(value):
    ret = 0
    if " " in value:
        value = value.split(" ")[0]
    if "." in value:
        ret = float(value)
    else:
        ret = int(value)
    return ret

def conditionsPreparsing(conditions):
    parsedConditions = []
    print("Conditions set to parsing: ",conditions)
    for condition in conditions:
        val = 0
        tempCond = {}
        tempCond["name"] = condition["name"]
        tempCond["isExtendable"] = condition["isExtendable"]
        if "%" in condition["value"]:
            tmp = condition["value"].split("%")[0]
            tempCond["isPercentage"] = True
            val = parseValue(tmp)
        else:
            tempCond["isPercentage"] = False
            val = parseValue(condition["value"])
        tempCond["value"] = val
        parsedConditions.append(tempCond)
    print("Parsed conditions: ",parsedConditions)
    return parsedConditions

def incomePreparsing(income, knownExpenses):
    expenses = 0
    for expense in knownExpenses:
        expenses += expense
    
    remainingAmount = income - expenses
    return remainingAmount

def budgetCreationGA(income,knownExpenses,conditions):
    max_gen = 300
    remainingAmount = incomePreparsing(income,knownExpenses)
    USABLE_AMOUNT = remainingAmount
    bestGenome = Genome([],0)
    print("Conditions from form: ",conditions)
    if remainingAmount < 0:
        return (False,{"annotation": "LOSS"})
    elif remainingAmount == 0:
        return (False,{"annotation": "EVEN"})
    else:
        conds = conditionsPreparsing(conditions)
        print("Conditions post parsing before new pop creation: ",conds)
        population = createNewPopulation(50,conds)
        generation = 0

        while generation < max_gen:
            for i in range(int(floor(len(population)/2))):
                population.append(reproduction(population,conds))

            for genom in population:
                if genom.fitness > THRESHOLD or genom.fitness < 0:
                    population.remove(genom)
            
            bestGenome = findBestGenome(population)

        ret = {}
        ret["annotation"] = ""
        calculatedExpenses = []
        for i in range(len(bestGenome.chromosomes)):
            tmp = {}
            tmp["category"] = conds[i].name
            if conds[i].isPercentage:
                tmp["sum"] = conds[i].value * USABLE_AMOUNT * bestGenome.chromosomes[i] / 100
            else:
                tmp["sum"] = conds[i].value * bestGenome.chromosomes[i]
            calculatedExpenses.append(tmp)
        if bestGenome.fitness != 0:
            tmp = {}
            tmp["sum"] = USABLE_AMOUNT - bestGenome.fitness
            tmp["category"] = "unassigned"
            calculatedExpenses.append(tmp)
        ret["calculatedExpenses"] = calculatedExpenses
        return (True,ret)