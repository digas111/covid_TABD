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
import time
import datetime

start_time = time.time()


conn = psycopg2.connect("dbname=tabd user=postgres password = 11223344Ab")
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

with open('E:\TrabalhoManel\Fac\TABD\covid_TABD\offsets3.csv', 'r') as csvFile:
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

for i in range(0,len(offsets)):
    for j in range(0,len(offsets[i])):
        if (offsets[i][j] != [0,0]):
            if (infectionPercentages[i][j] == 100):
                idDistrict = None
                sql = "select distrito from cont_aad_caop2018 where st_contains(proj_boundary, st_setsrid(st_point(" + str(offsets[i][j][0]) + ", " + str(offsets[i][j][1]) +"), 3763))"
                cursor_psql.execute(sql)
                results = cursor_psql.fetchall()
                if (results != []):
                    idDistrict = int(districts.get(results[0][0]))
                else:
                    print("PONTO FORA DO MAPA: " + str(offsets[i][j][0]) + " " + str(offsets[i][j][1]))
                if (idDistrict != None):
                    infectedByDistrict[i][idDistrict] +=1
                    k = i+1
                    while (k<len(offsets) and offsets[k][j] == [0,0]):
                        infectedByDistrict[k][idDistrict] += 1
                        k+=1

                    k = i+1
                    while (k<len(offsets)):
                        sql = "select distrito from cont_aad_caop2018 where st_contains(proj_boundary, st_setsrid(st_point(" + str(offsets[k][j][0]) + ", " + str(offsets[k][j][1]) +"), 3763))"
                        cursor_psql.execute(sql)
                        results = cursor_psql.fetchall()
                        if (results == []):
                            print("PONTO FORA DO MAPA TRATADO")
                            infectedByDistrict[k][idDistrict] += 1
                        else:
                            break
                        k+=1
                    

#####

if os.path.exists("simulateInfection.csv"):
    os.remove("simulateInfection.csv")

simulateInfectionf = open("simulateInfection.csv", "a")

for i in range(0,len(offsets)):
    firstPrint = True
    for j in range(0,len(offsets[i])):
        if (offsets[i][j] != [0,0]):
            if (firstPrint):
                simulateInfectionf.write(str(offsets[i][j][0]) + " " + str(offsets[i][j][1]) + " " + colors[i][j])
                firstPrint = False
            else:
                simulateInfectionf.write("," + str(offsets[i][j][0]) + " " + str(offsets[i][j][1]) + " " + colors[i][j])
    simulateInfectionf.write("\n")
simulateInfectionf.close()

#####

if os.path.exists("nInfected.csv"):
    os.remove("nInfected.csv")

nInfectedf = open("nInfected.csv", "a")

for infected in nInfected:
    nInfectedf.write(str(infected)+"\n")
nInfectedf.close()

#####

if os.path.exists("infectionsByDistrict.csv"):
    os.remove("infectionsByDistrict.csv")

infectionsByDistrictf = open("infectionsByDistrict.csv", "a")

for ts in infectionsByDistrict:
    infectionsByDistrictf.write(str(ts[0]))
    for district in range(1,len(ts)):
        infectionsByDistrictf.write("," + str(ts[district]))
    infectionsByDistrictf.write("\n")
infectionsByDistrictf.close()

#####

if os.path.exists("infectedByDistrict.csv"):
    os.remove("infectedByDistrict.csv")

infectedByDistrictf = open("infectedByDistrict.csv", "a")

for ts in infectedByDistrict:
    infectedByDistrictf.write(str(ts[0]))
    for j in range(1,len(ts)):
        infectedByDistrictf.write("," + str(ts[j]))
    infectedByDistrictf.write("\n")
infectedByDistrictf.close()


conn.close()

print("Ficheiros criados em: " + str(datetime.timedelta(seconds=(time.time() - start_time))))

