from os import walk
import csv
import ast

NUM_SIMULATIONS = 250


def readDataFiles():
    dataSet = {}
    for root, dirs, files in walk("./"):
        for file in files:
            if file.startswith('DATA'):
                f = open(file)
                reader = csv.reader(f, delimiter=';')
                dataDict = {}
                for row in reader:
                    if len(row) > 0 and not 'sep' in row[0]:
                        for i in range(len(row) - 1):
                            row[i+1] = ast.literal_eval(row[i+1])
                        
                        dataDict[row[0]] = row[1:]
                dataSet[file] = dataDict
    return dataSet


def shots(dataSet):
    """
        Returns a tuple of two dictionaries: shotsTaken, and shotsMade
        
        shotsTaken - A dictionary with Offense Formations as keys, and the total shots
            taken throughout all simulations and matchups for that formation as values
        shotsTaken - A dictionary with Offense Formations as keys, and the total shots made
            throughout all simulations and matchups for that formation as values
        offRangeTaken - A dictionary with Offense Formations as keys, and values as lists
            The list value has the following format:
                [ [defFormation, maxShotsTaken] , [defFormation, minShotsTaken] ]
        offRangeMade - Same as offRangeTaken, but with shots made instead
        
    """
    shotsTaken = {}
    shotsMade = {}
    offRangeTaken = {}
    offRangeMade = {}
    for matchup in dataSet.keys():
        offEnd = matchup.index('D', 1) - 2
        defEnd = matchup.index('.') - 1
        offFormation = matchup[5:offEnd + 1]
        defFormation = matchup[offEnd + 2:defEnd + 1]
        data = dataSet[matchup]
        
        for point in data.keys():
            if 'number of goal attempts' in point:
                try:
                    taken = sum(data[point])
                    shotsTaken[offFormation] += taken
                    if taken > offRangeTaken[offFormation][0][1]:
                        offRangeTaken[offFormation][0] = [defFormation, taken]
                    if taken < offRangeTaken[offFormation][1][1]:
                        offRangeTaken[offFormation][1] = [defFormation, taken]
                            
                except:
                    taken = sum(data[point])
                    shotsTaken[offFormation] = taken
                    offRangeTaken[offFormation] = [[defFormation, taken], [defFormation, taken]]
                     
            elif 'number of goals' in point:
                try:
                    made = sum(data[point])
                    shotsMade[offFormation] += made
                    if made > offRangeMade[offFormation][0][1]:
                        offRangeMade[offFormation][0] = [defFormation, made]
                    if made < offRangeMade[offFormation][1][1]:
                        offRangeMade[offFormation][1] = [defFormation, made]
                except:
                    made = sum(data[point])
                    shotsMade[offFormation] = made
                    offRangeMade[offFormation] = [[defFormation, made], [defFormation, made]]
                     
    return (shotsTaken, shotsMade, offRangeTaken, offRangeMade)


def bestFormation(dataSet):
    gamesWon = {}
    for matchup in dataSet.keys():
        offEnd = matchup.index('D', 1) - 2
        defEnd = matchup.index('.') - 1
        offFormation = matchup[5:offEnd + 1]
        defFormation = matchup[offend + 2:defEnd + 1]
        data = dataSet[matchup]
        
        for point in data.keys():
            if 'Game won?' in point:
                try:
                    gamesWon[offFormation] += sum(data[point])
                except:
                    gamesWon[offFormation] = sum(data[point])
                break
    return dictSort(gamesWon)[0][-1]



def swap(lst, shadowLst, i, j):
    temp = lst[j]
    shadowTemp = shadowLst[j]
    lst[j] = lst[i]
    shadowLst[j] = shadowLst[i]
    lst[i] = temp
    shadowLst[i] = shadowTemp


def expcdf(x, mu):
    return 1 - exp(-x/mu)


def partition(lst, shadowLst, m, k):
    if (k - m + 1) <= 1:
        return None
    pivot = lst[m]
    i = m
    j = m + 1
    
    # Precondition: Section of list <= i is less than or equal to the pivot
    #               lst[i] is the pivot
    #               For i < x < j, lst[x] is greater than the pivot
    #               For j <= x, lst[x] is unsorted
    while (j <= k):
        if lst[j] <= pivot:
            swap(lst, shadowLst, j, i)
            swap(lst, shadowLst, i + 1, j)
            i += 1
        j += 1
    return i


def quickSort(lst, shadowLst, m, k):
    if (k - m + 1) <= 1:
        return None
    pivot = partition(lst, shadowLst, m, k)
    quickSort(lst, shadowLst, m, pivot - 1)
    quickSort(lst, shadowLst, pivot + 1, k)


def dictSort(dct):
    keys = list(dct.keys())
    values = list(dct.values())
    quickSort(values, keys, 0, len(values) - 1)
    return (keys, values)
        
