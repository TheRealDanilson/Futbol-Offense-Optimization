import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rcParams
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
        ax.text(rect.get_x() + rect.get_width()/2., rect.get_y() + height, \
                '%d' % int(height), ha='center', va= 'bottom')


def shotsTakenMade():
    formationShotsTaken = []
    formationShotsMade =  []
    formationLabels = []
    
    #creating data points to be graphed
    for i in tuple(shotsTaken.items()):
        formationLabels += [i[0]]
        formationShotsTaken += [i[1]]
    for i in tuple(shotsMade.items()):
        formationShotsMade += [i[1]]
        
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
    
    
    
def formationPasses():
    colors = ('#AC3931', '#0B4F6C')
    formationLabels = []
    formationPasses = []
    
    for offFormation in passInformation[list(passInformation.keys())[0]]:
        formationLabels += [offFormation]
    #print(formationLabels)

    N = len(formationLabels)        
    ind = np.arange(N)
    width = .5
    
    #print(passInformation.items())

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
    #print(allPasses)    
    
        
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
    
    graphLabels(ax,'Total Passes per Formation','Formations','Passes',ind, width, xTick = formationLabels)
    
    ax.legend(allRects, tuple(passInformation.keys()),frameon=False, loc=( 1))

    for i in allRects:
        barLabels(ax, i)
        
    
def listAdd(lst1, lst2):
    for i in range(len(lst1)):
        lst1[i] += lst2[i]
        
        
        
def shotMapMissed():
    fig, ax = plt.subplots()
    background = plt.imread('Images/soccerField.png')
    ax.imshow(background, extent = (-45, 45, 0, 60))
    colors = ('r', 'g', 'b', 'k', 'm', 'y')
    i = 0
    for defFormation in shotsMap.keys():
        color = colors[i]
        positions = tuple(shotsMap[defFormation].keys())
        x = []
        y = []
        for position in positions:
            if shotsMap[defFormation][position] == 'o':
                x += [position[0]]
                y += [position[1]]
                
        plt.scatter(x, y, marker = '.', color = color)
        i += 1
        
    
def shotMapMade():
    fig, ax = plt.subplots()
    background = plt.imread('Images/soccerField.png')
    ax.imshow(background, extent = (-45, 45, 0, 60))
    colors = ('r', 'g', 'b', 'k', 'm', 'y')
    i = 0
    for defFormation in shotsMap.keys():
        color = colors[i]
        positions = tuple(shotsMap[defFormation].keys())
        x = []
        y = []
        for position in positions:
            if shotsMap[defFormation][position] == 'x':
                x += [position[0]]
                y += [position[1]]
                
        plt.scatter(x, y, marker = 'x', color = color)
        i += 1
        
    
    
def formationInterceptions():
    colors = ('#AC3931', '#0B4F6C')
    formationLabels = []
    formationInterceptions = []
    
    for defFormation in interceptionInformation[list(interceptionInformation.keys())[0]]:
        formationLabels += [defFormation]
    #print(formationLabels)

    N = len(formationLabels)        
    ind = np.arange(N)
    width = .5
    
    #print(interceptionInformation.items())

    allInterceptions = [None]*N
    i = 0
    for offFormation in interceptionInformation.keys():
        offDict = interceptionInformation[offFormation]
        for defFormation in offDict.keys():
            num = offDict[defFormation]
            try:
                allInterceptions[i].append(num)
            except:
                allInterceptions[i] = [num]
        i += 1
    #print(allInterceptions)    
    
        
    fig, ax = plt.subplots()
    allRects = []
    bottoms = [0]*N
    for i in range(N):
        if i == 0:
            newRect = ax.bar(ind, tuple(allInterceptions[i]), width, color = colors[i % 2])
        else:
            newRect = ax.bar(ind,tuple(allInterceptions[i]), width, bottom = bottoms)
        listAdd(bottoms, allInterceptions[i])
        allRects.append(newRect)
    
    graphLabels(ax,'Total Interceptions per Formation','Formations','Interceptions',ind, width, xTick = formationLabels)
    
    ax.legend(allRects, tuple(interceptionInformation.keys()),frameon=True, loc=( 1))

    for i in allRects:
        barLabels(ax, i)
        
    

def heatMap():
    lst = shotsByFormation.items()
    side = np.linspace(0, 5, 6)
    x, y = np.meshgrid(side, side)
    i = 0
    z = np.zeros((6,6))
    fig, ax = plt.subplots()
    offFormationOrder = shotsByFormation.keys()
    defFormationOrder = tuple(lst)[0][1].keys()
    for offFormation in offFormationOrder:
        offDict = shotsByFormation[offFormation]
        j = 0
        for shot in offDict.values():
            zVal = shot
            z[i][j] = zVal
            #ax.text(i, j, str(zVal) + '%', ha='center', va='center', color='k', size=16)
            j += 1
        i += 1
   #prop = fm.FontProperties(fname='/usr/share/fonts/OTF/MyriadPro_Bold.otf')
    offOrder = []
    defOrder = []
    for off in offFormationOrder:
        offOrder += [off[4:]]
    for deff in defFormationOrder:
        defOrder += [deff[4:]]
    ax.set_xticks(np.arange(6))
    ax.set_yticks(np.arange(6))
    ax.set_xlabel('Offenses', size = 26)
    ax.set_ylabel('Defenses', size = 26)
    ax.set_xticklabels(offOrder, size=12)
    ax.set_yticklabels(defOrder, size=12)
    ax.xaxis.set_label_coords(0.5, -0.05)
    ax.yaxis.set_label_coords(-.10, 0.5)
    ax.set_title('Goals per Matchup', size=30, fontweight='bold', y = 1.04)
    
    plt.imshow(z.T, cmap = 'Blues')
    cbar = plt.colorbar()
    cbar.ax.tick_params(labelsize=12)
    #fig.savefig('test.svg', dpi=300)
    return offFormationOrder, defFormationOrder
    #X, Y = np.meshgrid(xedges, yedges)
    #ax.pcolormesh(X, Y, heatmap.T)
        
        

def passingHeat():
    passInformationInverted = invertDict(passInformation)
    lst = passInformationInverted.items()
    side = np.linspace(0, 5, 6)
    x, y = np.meshgrid(side, side)
    i = 0
    z = np.zeros((6,6))
    fig, ax = plt.subplots()
    for offFormation in offFormationOrder:
        offDict = passInformationInverted[offFormation]
        j = 0
        for passes in offDict.values():
            zVal = passes
            z[i][j] = zVal
            #ax.text(i, j, str(zVal) + '%', ha='center', va='center', color='k', size=16)
            j += 1
        i += 1
    offOrder = []
    defOrder = []
    for off in offFormationOrder:
        offOrder += [off[4:]]
    for deff in defFormationOrder:
        defOrder += [deff[4:]]
    ax.set_xticks(np.arange(6))
    ax.set_yticks(np.arange(6))
    ax.set_xlabel('Offenses', size = 26)
    ax.set_ylabel('Defenses', size = 26)
    ax.set_xticklabels(offOrder, size=12)
    ax.set_yticklabels(defOrder, size=12)
    ax.xaxis.set_label_coords(0.5, -0.05)
    ax.yaxis.set_label_coords(-.10, 0.5)
    ax.set_title('Passes per Matchup', size=30, fontweight='bold',  y = 1.04)
    
    plt.imshow(z.T, cmap = 'Blues')
    cbar = plt.colorbar()
    cbar.ax.tick_params(labelsize=12)
    
    
def interceptionHeat():
    interceptionInformationInverted = invertDict(interceptionInformation)
    lst = interceptionInformationInverted.items()
    side = np.linspace(0, 5, 6)
    x, y = np.meshgrid(side, side)
    i = 0
    z = np.zeros((6,6))
    fig, ax = plt.subplots()
    for defFormation in defFormationOrder:
        defDict = interceptionInformationInverted[defFormation]
        j = 0
        for interceptions in defDict.values():
            zVal = interceptions
            z[i][j] = zVal
            #ax.text(i, j, str(zVal) + '%', ha='center', va='center', color='k', size=16)
            j += 1
        i += 1
    offOrder = []
    defOrder = []
    for off in offFormationOrder:
        offOrder += [off[4:]]
    for deff in defFormationOrder:
        defOrder += [deff[4:]]
    ax.set_xticks(np.arange(6))
    ax.set_yticks(np.arange(6))
    ax.set_xlabel('Defenses', size = 26)
    ax.set_ylabel('Offenses', size = 26)
    ax.set_xticklabels(defOrder, size=12)
    ax.set_yticklabels(offOrder, size=12)
    ax.xaxis.set_label_coords(0.5, -0.05)
    ax.yaxis.set_label_coords(-.10, 0.5)
    tit = ax.set_title('Interceptions per Matchup', size=30, fontweight='bold', y = 1.04)
    plt.imshow(z.T, cmap = 'Blues')
    cbar = plt.colorbar()
    cbar.ax.tick_params(labelsize=12) 


def invertDict(dct):
    lst = tuple(dct.items())
    internalKeys = lst[0][1].keys()
    inverted = {}
    for inner in internalKeys:
        inverted[inner] = {}
        for outer in dct.keys():
            inverted[inner][outer] = dct[outer][inner]
    return inverted
        


#Using readData
font_dirs = ['/usr/share/fonts/OTF']
font_files = fm.findSystemFonts(fontpaths=font_dirs)
font_list = fm.createFontList(font_files)
fm.fontManager.ttflist.extend(font_list)
#print(rcParams)
rcParams['font.family'] = 'Myriad Pro'


dataSet = readDataFiles()
shotsTaken, shotsMade, rangeTaken, rangeMade, shotsByFormation = shots(dataSet)
passInformation = passes(dataSet)
#print('Pass info', passInformation)
interceptionInformation = interceptions(dataSet)
shotsTakenMade()
formationPasses()
formationInterceptions()
best = bestFormation(dataSet)
shotsMap = shotMapData(dataSet, best)
shotMapMissed()
shotMapMade()
offFormationOrder, defFormationOrder = heatMap()
passingHeat()
interceptionHeat()
plt.show()

#fig.savefig('filename'.png)
# horizontal bar =  barh
