import numpy as np
import matplotlib.pyplot as plt
import psycopg2
import math
from matplotlib.animation import FuncAnimation
import datetime
import csv
from postgis import Polygon,MultiPolygon
from postgis.psycopg import register
import random

##########

infectingDistance = 50
infectingRate = 10
#percentage by frame

#####

offsets = []
infectedID = []
infectionPercentages = []
colors = []

taxisPorto = {161, 238, 110, 978, 306, 723, 247, 664, 187, 958}
taxisLisboa= {1602, 836, 1285, 872, 1163, 815, 1180, 817, 1500, 1564}
firstTaxiPorto = random.sample(taxisPorto,1)[0]
firstTaxiLisboa = random.sample(taxisLisboa,1)[0]


##########

#### FUNCTIONS ####

def infectTaxi(frame,row):

    global infectionPercentages
    global infectedID

    infectedID.append(row)
    for i in range(frame,len(infectionPercentages)):
        infectionPercentages[i][row]=100
        colors[i][row]="red"

###################

with open('offsets3.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        l = []
        inf = []
        color = []
        for j in row:
            x,y = j.split()
            x = float(x)
            y = float(y)
            l.append([x,y])
            inf.append(int(0))
            color.append("green")
        offsets.append(l)
        infectionPercentages.append(inf)
        colors.append(color)


# Infect first taxis
infectTaxi(0,firstTaxiPorto)
infectTaxi(0,firstTaxiLisboa)

for i in range(1,len(offsets)):
    for j in range(0,len(offsets[0])):
        if (offsets[i][j] != [0,0]):
            if (infectionPercentages[i][j] < 100):
                for ifid in infectedID:
                    dist = int(math.dist(offsets[i][j],offsets[i][ifid]))
                    if (dist < infectingDistance):
                        infectionPercentages[i][j] = infectionPercentages[i-1][j] + infectingRate
                if (infectionPercentages[i][j] >= 100):
                    infectTaxi(i,j)


for color in colors:
    print("%s" %(color[0]),end='')
    for c in color:
        print(",%s" %(c),end='')
    print("")


