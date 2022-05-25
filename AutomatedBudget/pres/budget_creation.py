from random import uniform,randrange
from numpy import floor


MUTATION_RATE = 1
MUTATION_REPEAT_COUNT = 2
CROSSOVER_RATE = 70

class Genome():
    def __init__(self,chromosomes,fitness):
        self.chromosomes=chromosomes
        self.fitness=fitness

def removeNones(arr):
    ret = []
    for a in arr:
        if a != None:
            ret.append(a)
    return ret

def evaluate(chromosomes,conditions):
    spentAmount = 0
    condMatch = 1
    for i in range(len(chromosomes)):
        if conditions[i]["isPercentage"]:
            spentAmount += conditions[i]["value"] * userIncome * chromosomes[i]
            condMatch *= chromosomes[i] * conditions[i]["value"]
        else:
            spentAmount += conditions[i]["value"] * chromosomes[i]
            condMatch *= (conditions[i]["value"] * chromosomes[i]) / conditions[i]["value"]
    return ((usableAmount - spentAmount) * condMatch)

def createNewPopulation(size,conditions):
    population = []
    for i in range(size):
        chromosomes = []
        for condition in conditions:
            if condition["isExtendable"]:
                chromosomes.append(uniform(0,5))
            else:
                chromosomes.append(uniform(0.0,1.0))

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

def mutation(chromo,conditions):
    for x in range(MUTATION_REPEAT_COUNT):
        idx = randrange(0, len(conditions) - 1)
        if conditions[idx]["isExtendable"]:
            chromo[idx] = uniform(0,5)
        else:
            chromo[idx] = uniform(0.0,1.0)
        
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
        child = mutation(child,conditions)
    
    newGenome = Genome(child,evaluate(child,conditions))
    return newGenome

def orderOneCrossover(parent1, parent2):
    size = len(parent1)
    child = [-1] * size

    point = randrange(1, size)

    for i in range(point):
        child[i] = parent1[i]

    for i in range(point, size):
        child[i] = parent2[i]


def reproduction(population,conditions):
    population = removeNones(population)
    parent1 = tournamentSelection(population, 10).chromosomes
    parent2 = tournamentSelection(population, 6).chromosomes
    cnt = 0
    while parent1 == parent2 and cnt < 50:
        parent2 = tournamentSelection(population, 6).chromosomes
        cnt += 1
    
    if randrange(0, 100)<CROSSOVER_RATE and len(parent1) > 2:
        return orderOneCrossover(parent1, parent2)
    else:
        return copyChromosomes(parent1,parent2,conditions)

def parseValue(value,isPercentage):
    ret = 0
    if " " in value:
        value = value.split(" ")[0]
    if "." in value:
        ret = float(value)
    else:
        ret = int(value)
    if isPercentage:
        ret /= 100
    return ret

def conditionsPreparsing(conditions):
    parsedConditions = []
    for condition in conditions:
        val = 0
        tempCond = {}
        tempCond["name"] = condition["name"]
        tempCond["isExtendable"] = condition["isExtendable"]
        if "%" in condition["value"]:
            tmp = condition["value"].split("%")[0]
            tempCond["isPercentage"] = True
            val = parseValue(tmp,tempCond["isPercentage"])
        else:
            tempCond["isPercentage"] = False
            val = parseValue(condition["value"],tempCond["isPercentage"])
        tempCond["value"] = val
        parsedConditions.append(tempCond)
    return parsedConditions

def incomePreparsing(income, knownExpenses):
    expenses = 0
    for expense in knownExpenses:
        expenses += expense
    
    remainingAmount = income - expenses
    return remainingAmount


def budgetCreationGA(income,knownExpenses,conditions, savings):
    max_gen = 1000
    remainingAmount = incomePreparsing(income,knownExpenses)
    global usableAmount 
    usableAmount = remainingAmount
    global userIncome
    userIncome = income
    bestGenome = Genome([],9999)
    if remainingAmount < 0:
        return (False,{"annotation": "LOSS"})
    elif remainingAmount == 0:
        return (False,{"annotation": "EVEN"})
    else:
        conds = conditionsPreparsing(conditions)
        population = createNewPopulation(50,conds)
        generation = 0
        bestGenome = findBestGenome(population)
        while generation < max_gen:
            popLength = int(floor(len(population)/2))
            for i in range(popLength):
                population.append(reproduction(population,conds))
            population.sort(key=lambda p:p.fitness)
            for i in range(popLength):
                population.remove(population[i])
            population = removeNones(population)
            bestGenome = findBestGenome(population)
            generation += 1
        ret = {}
        ret["annotation"] = ""
        calculatedExpenses = []
        for i in range(len(bestGenome.chromosomes)):
            tmp = {}
            tmp["category"] = conds[i]["name"]
            if conds[i]["isPercentage"]:
                tmp["sum"] = conds[i]["value"] * usableAmount * bestGenome.chromosomes[i]
            else:
                tmp["sum"] = conds[i]["value"] * bestGenome.chromosomes[i]
            calculatedExpenses.append(tmp)
        if (usableAmount - sum(expense["sum"] for expense in calculatedExpenses)) != 0:
            tmp = {}
            tmp["sum"] = usableAmount - sum(expense["sum"] for expense in calculatedExpenses)
            tmp["category"] = "unassigned"
            calculatedExpenses.append(tmp)
        ret["calculatedExpenses"] = calculatedExpenses
        return (True,ret)