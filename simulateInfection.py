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

districts = {
    "AVEIRO" : "0",
    "BEJA" : "1",
    "BRAGA" : "2",
    "BRAGANÇA" : "3",
    "CASTELO BRANCO" : "4",
    "COIMBRA" : "5",
    "ÉVORA" : "6",
    "FARO" : "7",
    "GUARDA" : "8",
    "LEIRIA" : "9",
    "LISBOA" : "10",
    "PORTALEGRE" : "11",
    "PORTO" : "12",
    "SANTARÉM" : "13",
    "SETÚBAL" : "14",
    "VIANA DO CASTELO" : "15",
    "VILA REAL" : "16",
    "VISEU" : "17"
}

# sql = "select distrito from cont_aad_caop2018 where st_contains(proj_boundary, st_setsrid(st_point(" + str(pontoX) + ", " + str(pontoY) +"), 3763))"

taxisPorto = {161, 238, 110, 978, 306, 723, 247, 664, 187, 958}
taxisLisboa= {1602, 836, 1285, 872, 1163, 815, 1180, 817, 1500, 1564}
firstTaxiPorto = random.sample(taxisPorto,1)[0]
firstTaxiLisboa = random.sample(taxisLisboa,1)[0]

##########

#### FUNCTIONS ####

def updateInfectedByDistrict(time):
    global infectedByDistrict

    conn = psycopg2.connect("dbname=postgres user=postgres")
    register(conn)
    cursor_psql = conn.cursor()


    for id in infectedID:
        sql = "select distrito from cont_aad_caop2018 where st_contains(proj_boundary, st_setsrid(st_point(" + str(offsets[time][id][0]) + ", " + str(offsets[time][id][1]) +"), 3763))"
        cursor_psql.execute(sql)
        results = cursor_psql.fetchall()
        print(int(districts.get(results[0][0])))
        # districtID = int(districts.get(results[0][0]))
        # infectedByDistrict[time][districtID] += 1

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
        
        districtaux = []
        for district in districts:
            districtaux.append(0)
        infectedByDistrict.append(districtaux)

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
    #updateInfectedByDistrict(i)
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

#print(infectedByDistrict)

# f = open("simulateInfection.csv", "w")



# f.write("Woops! I have deleted the content!")
# f.close()

for i in range(0,len(offsets)):
    print("%f %f %s" %(offsets[i][0][0],offsets[i][0][1],colors[i][0]),end='')
    for j in range(0,len(offsets[i])):
        print(",%f %f %s" %(offsets[i][j][0],offsets[i][j][1],colors[i][j]),end='')
    print("")
