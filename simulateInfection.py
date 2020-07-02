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
import os
import shutil
import time
import datetime

start_time = time.time()

conn = psycopg2.connect("dbname=postgres user=postgres")
register(conn)
cursor_psql = conn.cursor()

##########

infectingDistance = 80
infectingRate = 20
#percentage by frame

##########

#####

offsets = []
infectedID = []
infectionPercentages = []
colors = []
nInfected = []
infectedByDistrict = []
infectionsByDistrict = []

#####

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

taxisPorto = {161, 238, 110, 978, 306, 723, 247, 664, 187, 958}
taxisLisboa= {1602, 836, 1285, 872, 1163, 815, 1180, 817, 1500, 1564}
firstTaxiPorto = random.sample(taxisPorto,1)[0]
firstTaxiLisboa = random.sample(taxisLisboa,1)[0]

##########

#### FUNCTIONS ####

def infectTaxi(frame,row):

    global infectionPercentages
    global infectedID
    global nInfected
    global infectionsByDistrict

    numberInfect = nInfected[frame]+1

    infectedID.append(row)

    idDistrict = None

    sql = "select distrito from cont_aad_caop2018 where st_contains(proj_boundary, st_setsrid(st_point(" + str(offsets[frame][row][0]) + ", " + str(offsets[frame][row][1]) +"), 3763))"
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()
    if (results != []):
        idDistrict = int(districts.get(results[0][0]))
    else:
        print("PONTO FORA DO MAPA: " + str(offsets[frame][row][0]) + " " + str(offsets[frame][row][1]))

    for i in range(frame,len(infectionPercentages)):
        if (idDistrict != None):
            infectionsByDistrict[i][idDistrict] += 1
        nInfected[i] = numberInfect
        infectionPercentages[i][row]=100
        colors[i][row]="#cd0000" #red

###################

with open('offsets3.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        nInfected.append(0)
        infectionsByDistrict.append([0]*len(districts))
        infectedByDistrict.append([0]*len(districts))
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

# Percorrer primeiro por coluna e depois por linha para tornar o ficheiro mais eficiente
#### Infetados por distrito ####

for j in range(0,len(offsets[0])):

    i=0
    results = None

    while (i<len(offsets) and (offsets[i][j] == [0,0] or infectionPercentages[i][j] < 100)):
        i+=1

    if (i<len(offsets)):
        sql = "select distrito from cont_aad_caop2018 where st_contains(proj_boundary, st_setsrid(st_point(" + str(offsets[i][j][0]) + ", " + str(offsets[i][j][1]) +"), 3763))"
        cursor_psql.execute(sql)
        results = cursor_psql.fetchall()

    while (i<len(offsets) and (offsets[i][j] == [0,0] or results == [])):
        i+=1
        sql = "select distrito from cont_aad_caop2018 where st_contains(proj_boundary, st_setsrid(st_point(" + str(offsets[i][j][0]) + ", " + str(offsets[i][j][1]) +"), 3763))"
        cursor_psql.execute(sql)
        results = cursor_psql.fetchall()

    while(i<len(offsets)):

        if (results != [] and offsets[i][j] != [0,0]):
            idDistrict = int(districts.get(results[0][0]))

        infectedByDistrict[i][idDistrict] += 1

        i+=1
        if (i<len(offsets)):
            sql = "select distrito from cont_aad_caop2018 where st_contains(proj_boundary, st_setsrid(st_point(" + str(offsets[i][j][0]) + ", " + str(offsets[i][j][1]) +"), 3763))"
            cursor_psql.execute(sql)
            results = cursor_psql.fetchall()
        
                    
conn.close()

##### WRITE TO FILES #####

folder = os.getcwd()+"/data/"

try:
    os.mkdir(folder)
except OSError:
    try:
        shutil.rmtree(folder)
    except OSError:
        print("ERROR CREATING FOLDER")
    try:
        os.mkdir(folder)
    except OSError:
        print("ERROR CREATING FOLDER")

# def writeSimulateInfection():

#### Create File with offsets and infections #### -> new thread

with open(folder + 'simulateInfection.csv', 'w', newline='') as sif:
    sifw = csv.writer(sif)
    for rf, rc in zip(offsets,colors):
        row = []
        for cf, cc in zip(rf,rc):
            if (cf != [0,0]):
                row.append(str(cf[0]) + " " + str(cf[1]) + " " + cc)
        sifw.writerow(row)

# def writeNInfected():

#### Create file with number of infected an file with R #### -> new thread

with open(folder + 'infections.csv', 'w', newline='') as nif, open(folder + 'rvalues.csv', 'w', newline='') as rv:

    nifw = csv.writer(nif)
    rvw = csv.writer(rv)

    nifw.writerow([nInfected[0]])
    rvw.writerow([0])

    for i in range(1,len(nInfected)):
        nifw.writerow([nInfected[i]])
        rvw.writerow([(nInfected[i]-nInfected[i-1]) / nInfected[i-1]])


# def writeInfectionsByDistrict():

#### Create file with new infections by dristrict #### -> new thread

with open(folder + 'infectionsByDistrict.csv', 'w', newline='') as isbdf:
    isbdfw = csv.writer(isbdf)
    for row in infectedByDistrict:
        isbdfw.writerow(row)

# def writeInfectedByDistrict():

#### Create file with infected by district #### -> new thread

with open(folder + 'infectedByDistrict.csv', 'w', newline='') as idbdf:
    idbdfw = csv.writer(idbdf)
    for row in infectedByDistrict:
        idbdfw.writerow(row)

print("Ficheiros criados em: " + str(datetime.timedelta(seconds=(time.time() - start_time))))

