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

infectingDistance = 80
infectingRate = 20
#percentage by frame

#####

offsets = []
infectedID = []
infectionPercentages = []
colors = []
nInfected = []
infectedByDistrict = []

distritos = {
    "1" : "AVEIRO",
    "2" : "BEJA",
    "3" : "BRAGA",
    "4" : "BRAGANÇA",
    "5" : "CASTELO BRANCO",
    "6" : "COIMBRA",
    "7" : "ÉVORA",
    "8" : "FARO",
    "9" : "GUARDA",
    "10" : "LEIRIA",
    "11" : "LISBOA",
    "12" : "PORTALEGRE",
    "13" : "PORTO",
    "14" : "SANTARÉM",
    "15" : "SETÚBAL",
    "16" : "VIANA DO CASTELO",
    "17" : "VILA REAL",
    "18" : "VISEU"
}

# sql = "select distrito from cont_aad_caop2018 where st_contains(proj_boundary, st_setsrid(st_point(" + str(pontoX) + ", " + str(pontoY) +"), 3763))"

taxisPorto = {161, 238, 110, 978, 306, 723, 247, 664, 187, 958}
taxisLisboa= {1602, 836, 1285, 872, 1163, 815, 1180, 817, 1500, 1564}
firstTaxiPorto = random.sample(taxisPorto,1)[0]
firstTaxiLisboa = random.sample(taxisLisboa,1)[0]

##########

#### FUNCTIONS ####

def updateInfectedByDistrict:



def infectTaxi(frame,row):

    global infectionPercentages
    global infectedID
    global nInfected

    numberInfect = nInfected[frame]+1

    infectedID.append(row)
    for i in range(frame,len(infectionPercentages)):
        nInfected[i] = numberInfect
        infectionPercentages[i][row]=100
        colors[i][row]="#cd0000" #red

###################

with open('offsets3.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        nInfected.append(0)
        l = []
        inf = []
        color = []
        for j in row:
            x,y = j.split()
            x = float(x)
            y = float(y)
            l.append([x,y])
            inf.append(int(0))
            color.append("#008000") #green
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
                        colors[i][j] = "black"
                if (infectionPercentages[i][j] >= 100):
                    infectTaxi(i,j)


for i in range(0,len(offsets)):
    print("%d,%f %f %s" %(nInfected[i],offsets[i][0][0],offsets[i][0][1],colors[i][0]),end='')
    for j in range(0,len(offsets[i])):
        print(",%f %f %s" %(offsets[i][j][0],offsets[i][j][1],colors[i][j]),end='')
    print("")
