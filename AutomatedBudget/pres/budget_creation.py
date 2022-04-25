class ParsedCondition():
    name = ""
    isExtendable = False
    isPercentage = False
    value = 0

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

def budgetCreationGA(income,knownExpenses,conditions):
    expenses = 0
    for expense in knownExpenses:
        expenses += expense.sum
    
    remainingAmount = income - expenses

    if remainingAmount < 0:
        return (False,{"annotation": "LOSS"})
    elif remainingAmount == 0:
        return (False,{"annotation": "EVEN"})
    else:
        conds = conditionsPreparsing(conditions)
