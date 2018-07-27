import numpy as np
import matplotlib.pyplot as plt
from readData import *

def graphLabels(ax,title,xAxis,yAxis,ind,width,xTick = ""):
    """
    Labels Title, X Axis and X Ticks, Y Axis and Y Ticks)
    """
    ax.set_title(title)
    ax.set_xlabel(xAxis)
    ax.set_ylabel(yAxis)
    ax.set_xticks(ind)
    ax.set_xticklabels(xTick)
    #ax.set_xticklabels(yTick )

def barLabels(ax, rects):
    """
    Attaches a text label above each bar desplaying the heights
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., rect.get_y() + .5 + height, \
                '%d' % int(height), ha='center', va= 'bottom')


def shotsTakenMade():
    formationShotsTaken = []
    formationShotsMade =  []
    formationLabels = []
    
    #creating data points to be graphed
    for i in tuple(shotsTaken.items()):
        formationLabels += [i[0]]
        formationShotsTaken += [i[1]/6]
    for i in tuple(shotsMade.items()):
        formationShotsMade += [i[1]/6]
        
    N = len(shotsTaken)        
    ind = np.arange(N)
    width = .5
    
    fig, ax = plt.subplots()
    print(formationShotsTaken, formationShotsMade)
    rects1 = ax.bar(ind, tuple(formationShotsTaken), width, color ='#AC3931')
    rects2 = ax.bar(ind, tuple(formationShotsMade), width, color = '#0B4F6C')
    
    graphLabels(ax,'Average Shots over all Matchups','Formations','Shots Average',ind, width, xTick = formationLabels)
    
    ax.legend((rects1[0],rects2[0]), ('Shots Taken', 'Goals Made'),frameon=False)

    barLabels(ax, rects1)
    barLabels(ax, rects2)
    
    #fig.savefig('test.png')
    
    plt.show()
    
    
def formationPasses():
    colors = ('#AC3931', '#0B4F6C')
    formationLabels = []
    formationPasses = []
    
    for offFormation in passInformation[list(passInformation.keys())[0]]:
        formationLabels += [offFormation]
    print(formationLabels)

    N = len(formationLabels)        
    ind = np.arange(N)
    width = .5
    
    print(passInformation.items())

    allPasses = [None]*N
    i = 0
    for defFormation in passInformation.keys():
        defDict = passInformation[defFormation]
        for offFormation in defDict.keys():
            num = defDict[offFormation]
            try:
                allPasses[i].append(num)
            except:
                allPasses[i] = [num]
        i += 1
    print(allPasses)    
    
        
    fig, ax = plt.subplots()
    allRects = []
    allPasses[:N - 3]
    bottoms = [0]*N
    for i in range(N):
        if i == 0:
            newRect = ax.bar(ind, tuple(allPasses[i]), width, color = colors[i % 2])
        else:
            newRect = ax.bar(ind,tuple(allPasses[i]), width, bottom = bottoms)
        listAdd(bottoms, allPasses[i])
        allRects.append(newRect)
    
    graphLabels(ax,'Total Passes per Formation','Passes','Formations',ind, width, xTick = formationLabels)
    
    ax.legend(allRects, tuple(passInformation.keys()),frameon=False, loc=(1, 1))

    for i in allRects:
        barLabels(ax, i)
        
    plt.show()
    
def listAdd(lst1, lst2):
    for i in range(len(lst1)):
        lst1[i] += lst2[i]

#Using readData
dataSet = readDataFiles()
#shotsTaken, shotsMade, rangeTaken, rangeMade = shots(dataSet)
passInformation = passes(dataSet)

#shotsTakenMade()
formationPasses()

#fig.savefig('filename'.png)
# horizontal bar =  barh
