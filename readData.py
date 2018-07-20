from os import walk
import csv
import ast


def readData():
    dataSet = {}
    for root, dirs, files in walk("./"):
        for file in files:
            if file.startswith('DATA'):
                f = open(file)
                reader = csv.reader(f, delimiter=';')
                dataDict = {}
                for row in reader:
                    for i in range(len(row) - 1):
                        row[i+1] = ast.literal_eval(row[i+1])
                    dataDict[row[0]] = row[1:]
                dataSet[file] = dataDict
    return dataSet


def shots(dataSet):
    shotsTaken = {}
    shotsMade = {}
    for matchup in dataSet.keys():
        offEnd = matchup.index('D', 1) - 2
        defEnd = matchup.index('.') - 1
        offFormation = matchup[5:offEnd + 1]
        defFormation = matchup[offend + 2:defEnd + 1]
        data = dataSet[matchup]
        
        for point in data.keys():
            if 'number of goal attempts' in point:
                try:
                    shotsTaken[offFormation] += sum(data[point])
                except:
                    shotsTaken[offFormation] = sum(data[point])
            elif 'number of goals' in point:
                try:
                    shotsMade[offFormation] += sum(data[point])
                except:
                    shotsMade[offFormation] = sum(data[point])
                    
    return (shotsTaken, shotsMade)
