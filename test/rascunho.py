import numpy as np
import matplotlib.pyplot as plt
import psycopg2
import math
from matplotlib.animation import FuncAnimation
import datetime
import csv
from postgis import Polygon,MultiPolygon
from postgis.psycopg import register
from random import randrange

debug = False

mindist = 99999999999999999

##########

infectingDistance = 50000
infectingRate = 10
#percentage by frame

##########

offsets = []
infected = []
rateOfInfection = []


##########################
##      FUNCTIONS       ##
##########################
def printDebugg(text):
    if(debug):
        print(text)

def infectTaxi(frame,row):
    global rateOfInfection
    infected.append(row)
    for i in range(frame,len(rateOfInfection)):
        rateOfInfection[i][row]=100

def distance(p1,p2):
    global mindist

    p1[0] = int(p1[0])
    p1[1] = int(p1[1])
    p2[0] = int(p2[0])
    p2[1] = int(p2[1])

    dist = int(math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) ))

    # if (dist != 0 and dist < mindist):
    #     mindist = dist

    #print("dist:" + str(dist))
    return dist

def simulateInfections():
    global offsets
    global infected
    global rateOfInfection

    printDebugg("Entered simulateInfections")
    for i in range(0,len(offsets)):
        print(rateOfInfection[i])
        for j in range(0,len(offsets[0])):
            #print(rateOfInfection[i])
            printDebugg("rateOfInfection[" + str(i) + "][" + str(j) + "]=" + str(rateOfInfection[i][j]))
            # if (rateOfInfection[i][j] < 100):
            nearInfected=False
            for inf in infected:
                printDebugg("INFECTED:" + str(inf))
                printDebugg("**CALL DISTANCE**")
                if (distance(offsets[i][j],offsets[i][inf]) <= infectingDistance):
                    printDebugg("**** INFECT ****")
                    #print("rateOfInfection[" + str(i) + "][" + str(j) + "]=" + str(rateOfInfection[i][j]))
                    rateOfInfection[i][j] = rateOfInfection[i][j] + infectingRate
                    #print("rateOfInfection[" + str(i) + "][" + str(j) + "]=" + str(rateOfInfection[i][j]))
                    nearInfected=True
            # if(nearInfected==False):
            #     rateOfInfection[i][j] = 0
            if (rateOfInfection[i][j] >= 100):
                infectTaxi(i,j)




#####################

def main():

    global offsets
    global infected
    global rateOfInfection



    with open('offsets3.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            l = []
            inf = []
            for j in row:
                x,y = j.split()
                x = float(x)
                y = float(y)
                l.append([x,y])
                inf.append(int(0))
            offsets.append(l)
            rateOfInfection.append(inf)


    firstInfectedIndex = randrange(0, len(offsets[0])-1)


    # print(len(offsets))
    # print(len(offsets[0]))

    # defenir primeiro como infetado
    infectTaxi(0,firstInfectedIndex)

    # for r in rateOfInfection:
    #     print(r)
  
    # simular infeções
    simulateInfections()

    for r in rateOfInfection:
        print(r)


    print("infected:")
    print(infected)
    # print("min_dist")
    # print(mindist)

    # for r in rateOfInfection:
    #     print(r,end='')

    # print(rateOfInfection[0])

    



    # if (debug):
    #     print(len(offsets[0]))
    #     # print(offsets[1])
    #     print(firstInfectedIndex)

    #     for r in rateOfInfection:
    #         print(r)




# Calculate the Euclidean distance  
# between points P and Q 
# eDistance = math.dist([Px, Py], [Qx, Qy]) 
# print(eDistance) 




if __name__ == "__main__":
    main()
