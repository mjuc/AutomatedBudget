from random import random
from re import A


MUTATION_RATE = 1
MUTATION_REPEAT_COUNT = 2
CROSSOVER_RATE = 70
THRESHOLD = 1000
USABLE_AMOUNT = 0

class ParsedCondition():
    name = ""
    isExtendable = False
    isPercentage = False
    value = 0

class Genome():
    chromosomes = []
    fitness = 9999

def evaluate(chromosomes,conditions):
    spentAmount = 0
    for i in range(len(chromosomes)):
        if conditions[i].isPercentage:
            spentAmount += conditions[i].value * USABLE_AMOUNT * chromosomes[i]
        else:
            spentAmount += conditions[i].value * chromosomes[i]
    return USABLE_AMOUNT - spentAmount

def createNewPopulation(size,conditions):
    population = []
    for i in range(size):
        newGenome = Genome()
        for condition in conditions:
            if condition.isExtendable :
                newGenome.chromosomes.append(random(0,5))
            else:
                newGenome.chromosomes.append(random())

        newGenome.fitness = evaluate(newGenome.chromosomes,conditions)
        population.append(newGenome)

def findBestGenome(population):
    allFitness = [i.fitness for i in population]
    bestFitness = min(allFitness)
    return population[allFitness.index(bestFitness)]

def tournamentSelection(population,k):
    selected = [population[random.randrange(0, len(population))] for i in range(k)]
    bestGenome = findBestGenome(selected)
    return bestGenome

def swapMutation(chromo):
    for x in range(MUTATION_REPEAT_COUNT):
        p1, p2 = [random.randrange(1, len(chromo) - 1) for i in range(2)]
        while p1 == p2:
            p2 = random.randrange(1, len(chromo) - 1)
        log = chromo[p1]
        chromo[p1] = chromo[p2]
        chromo[p2] = log
    return chromo

def copyChromosomes(parent1,parent2):
    size = len(parent1)
    child = [-1] * size
    
    for i in range(size):
        if random.randrange(0,1)==0:
            child[i]=parent1[i]
        else:
            child[i]=parent2[i]
    
    if random.randrange(0, 100) < MUTATION_RATE:
        pass
        child = swapMutation(child)
    
    newGenome = Genome()
    newGenome.chromosomes = child
    newGenome.fitness = evaluate(child)
    return newGenome

def orderOneCrossover(parent1, parent2):
    size = len(parent1)
    child = [-1] * size

    child[0], child[size - 1] = 0, 0

    point = random.randrange(5, size - 4)

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

def reproduction(population):
    parent1 = tournamentSelection(population, 10).chromosomes
    parent2 = tournamentSelection(population, 6).chromosomes
    while parent1 == parent2:
        parent2 = tournamentSelection(population, 6).chromosomes
    
    if random.randrange(0, 100)<CROSSOVER_RATE:
        return orderOneCrossover(parent1, parent2)
    else:
        return copyChromosomes(parent1,parent2)

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
    for condition in conditions:
        val = 0
        tempCond = ParsedCondition()
        tempCond.name = condition.name
        tempCond.isExtendable = condition.isExtendable
        if "%" in condition.value:
            tmp = condition.value.split("%")[0]
            tempCond.isPercentage = True
            val = parseValue(tmp)
        else:
            val = parseValue(condition.value)
        tempCond.value = val
        parsedConditions.append(tempCond)
    
    return parsedConditions

def incomePreparsing(income, knownExpenses):
    expenses = 0
    for expense in knownExpenses:
        expenses += expense.sum
    
    remainingAmount = income - expenses
    return remainingAmount

def budgetCreationGA(income,knownExpenses,conditions):
    max_gen = 300
    remainingAmount = incomePreparsing(income,knownExpenses)
    USABLE_AMOUNT = remainingAmount
    bestGenome = Genome()
    if remainingAmount < 0:
        return (False,{"annotation": "LOSS"})
    elif remainingAmount == 0:
        return (False,{"annotation": "EVEN"})
    else:
        conds = conditionsPreparsing(conditions)
        population = createNewPopulation(50,conds)
        generation = 0

        while generation < max_gen:
            for i in range(len(population)/2):
                population.append(reproduction(population))

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
                tmp["sum"] = conds[i].value * USABLE_AMOUNT * bestGenome.chromosomes[i]
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