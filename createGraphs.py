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
        ax.text(rect.get_x() + rect.get_width()/2., .5 + height, \
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
    rects1 = ax.bar(ind, tuple(formationShotsTaken), width, color ='#AC3931')
    rects2 = ax.bar(ind, tuple(formationShotsMade), width, color = '#0B4F6C')
    
    graphLabels(ax,'Goals','Formations','Shots',ind, width, xTick = formationLabels)
    
    ax.legend((rects1[0],rects2[0]), ('Shots Taken', 'Goals Made'),frameon=False)

    barLabels(ax, rects1)
    barLabels(ax, rects2)
    
    #fig.savefig('test.png')
    
    plt.show()
    
    
def formationPasses():
    
    formationLabels = []
    for i in tuple(passes.items()):
            formationLabels += [i[0]]

    N = len(formationLabels)        
    ind = np.arange(N)
    width = .5
    
    formationPasses = [] * N
    for i in range(N):
        for j in tuple(passes.items()):
            formationPasses[i] += [j[1][i]]
        
    fig, ax = plt.subplots()
    
    allRects = [] 
    for i in range(formationPasses):
        if i == 0:
            rects = ax.barh(ind, tuple(i[i]), width, color ='#AC3931')
        else:
            rects = ax.barh(ind,tuple(i[i]), width, color = 'r', bottom = formationPasses[i-1])
        allRects.append(rects)
    
    graphLabels(ax,'Total Passes per Formation','Passes','Formations',ind, width, xTick = formationLabels)
    
    ax.legend((rects1[0],rects2[0]), ('Shots Taken', 'Goals Made'),frameon=False)

    for i in allRects:
        barLabels(ax, i)
    
#Using readData
dataSet = readDataFiles()
shotsTaken, shotsMade, rangeTaken, rangeMade = shots(dataSet)
shotsTakenMade()
#fig.savefig('filename'.png)
# horizontal bar =  barh
