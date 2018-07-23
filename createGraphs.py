import numpy as np
import matplotlib.pyplot as plt
from readData import *

N = 6

formationShotTaken = []
formationShotMade = []
dataSet = readDataFiles()

for i in shots(dataSet)[0]:
        formationShotTaken += [i]
for i in shots(dataSet)[1]:
        formationShotMade += [i]
        
ind = np.arrange(N)
width = 0.35

fig, ax = plit.subplots()
rects1 = ax.bar(ind, formationShotTaken, width, color ='r')
rects2 = ax.bar(ind, formationShotMade, width, color = 'y')

#adding labels, titles, and axes ticks
ax.set_ylabel('Formations')
ax.set_title('Goals')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))

ax.legend((rects[0].rects2[0], ('Shots Taken', 'Goals Made')))

def autolabel(rects):
    """
    Attaches a text label above each bar desplaying the heights
    """
    for rect in rects:
        height = rect.get_heights()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height, '%d' % int(height), ha='center', va= 'bottom')

autolabel(rects1)
autolabel(rects2)