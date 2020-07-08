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
import curses
from progress.bar import IncrementalBar
from progress.spinner import Spinner
import menus


# Directory where files will be saved
subfolder = "/data/"

##########

infectingDistance = 50
infectingRate = 20 #percentage by frame

# Infected before preventive measures are taken
# If negative no measures will be taken
infectedBeforeMeasures = -1

# Applys preventive measures
def measures():

    global infectingDistance
    global infectingRate

    infectingDistance = infectingDistance/2
    infectingRate = infectingRate/2

# Connect to Database
conn = psycopg2.connect("dbname=postgres user=postgres")
register(conn)
cursor_psql = conn.cursor()

# Index of taxis that are infected from the start
startingInfected = []

# Offsetds of the taxis
offsets = []

# Saves index of infected taxis
infectedID = []

# Saves percentage of infections of each taxi in each frame
infectionPercentages = []

# Saves r for each hour
r = []

# Color of each taxi in each frame (corresponde to infection rate)
colors = []

#Nº infected for each frame
nInfected = []

#Nº infected taxis for district for each frame
# If car moves to another district the counter is updated
infectedByDistrict = []

# Nº taxis that got infected in each district for each frame
infectionsByDistrict = []

# Associates each district to the column that representes it in infectedByDistrict and infectionsByDistrict
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

# First 10 taxis to appear in Porto
taxisPorto = [161, 238, 110, 978, 306, 723, 247, 664, 187, 958]

# First 10 taxis to appear in Lisboa
taxisLisboa= [1602, 836, 1285, 872, 1163, 815, 1180, 817, 1500, 1564]

#### FUNCTIONS ####

# Infect a taxi from a specified frame until the last frame
def infectTaxi(frame,row):

    global infectionPercentages
    global infectedID
    global nInfected
    global infectionsByDistrict
    global cursor_psql

    # Nº of total infected taxis
    numberInfect = nInfected[frame]+1

    # Takes preventive measures if start number of infections is reached
    # If no measures are to be taken infectedBeforeMeasures is negative so the condition is always false
    if numberInfect == infectedBeforeMeasures:
        measures()

    # Add the index of the taxi to the list of infected taxis
    infectedID.append(row)

    # Saves the index of the district
    # Is None if car isn't in any district (error in the map)
    idDistrict = None

    # Query to get the district where the car is at the moment of infection
    sql = "select distrito from cont_aad_caop2018 where st_contains(proj_boundary, st_setsrid(st_point(" + str(offsets[frame][row][0]) + ", " + str(offsets[frame][row][1]) +"), 3763))"
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall() # result saves the name of the district in result[0][0]

    # If the car is in a district
    if (results != []):
        # Save index of the district
        idDistrict = int(districts.get(results[0][0])) 
    else:
        # Print message to console with the point the is out of the map
        print("PONTO FORA DO MAPA: " + str(offsets[frame][row][0]) + " " + str(offsets[frame][row][1]))

    # For everyframe since the infection
    for i in range(frame,len(infectionPercentages)):
        if (idDistrict != None):
            # Number of infections in district goes up by one
            infectionsByDistrict[i][idDistrict] += 1
        # Total number of infected goes up by one
        nInfected[i] = numberInfect
        # Probability of infection is 100%
        infectionPercentages[i][row]=100
        # Infected cars in displayed in red
        colors[i][row]="#cd0000" #red

# Gets geneation settings from user
# Starting point can be: Porto and Lisboa, Porto or Lisboa
# Measures can be taken or not
# If they are to be taken user gives nº infectied before measures take place

def getGenerationSettings(stdscr):

    global subfolder
    global infectedBeforeMeasures

    starting = menus.getStartingOptions(stdscr)

    if starting == 1: # Porto and Lisboa
        startingInfected.append(random.choice(taxisPorto))
        startingInfected.append(random.choice(taxisLisboa))
        subfolder += "PortoLisboa/"
    elif starting == 2: # Porto
        startingInfected.append(random.choice(taxisPorto))
        subfolder += "Porto/"
    elif starting == 3: # Lisboa
        startingInfected.append(random.choice(taxisLisboa))
        subfolder += "Lisboa/"
    else: # Cancel
        exit(0)

    infectedBeforeMeasures = menus.precautionaryMeasures(stdscr)

    if infectedBeforeMeasures >= 0: # Taking measures
        # Data is saved in a folder which name is the nº infected before measures are taken
        subfolder += str(infectedBeforeMeasures) + "/"
    if infectedBeforeMeasures == -2: # Cancel
        exit(0)

###################

# Display the menus to choose the genartion options
curses.wrapper(getGenerationSettings)

# Save inicial time to calculate run time
start_time = time.time()

# Opens file to count number of rows
with open('offsets3.csv', 'r') as csvFile:
    nrows = sum(1 for line in csv.reader(csvFile))

# Read Offsets and save them in memory
with open('offsets3.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    # Starts incremental bar
    with IncrementalBar(menus.offstestext, max= nrows, suffix = menus.suffix) as bar:
        for row in reader:
            # All cars start as not infected
            nInfected.append(0)
            infectionsByDistrict.append([0]*len(districts))
            infectedByDistrict.append([0]*len(districts))
            l = []
            inf = []
            color = []
            for column in row:
                x,y = column.split()
                x = float(x)
                y = float(y)
                l.append([x,y])
                inf.append(int(0))
                color.append("#008000") #green
            offsets.append(l)
            infectionPercentages.append(inf)
            colors.append(color)
            bar.next() # Advange the progress and update bar
        
# Infect the fisrt taxis
for taxi in startingInfected:
    infectTaxi(0,taxi)

# Simulate virus propagation
with IncrementalBar(menus.simulatevirustext, max= len(offsets)-1, suffix = menus.suffix) as bar:
    rPercentagesAux = 0
    hourloop = 0
    for i in range(1,len(offsets)):
        for j in range(0,len(offsets[0])):
            if (offsets[i][j] != [0,0]):
                if (infectionPercentages[i][j] < 100):
                    if hourloop == 360:
                        hourloop = 0
                        r.append(rPercentagesAux/100/nInfected[i])
                        rPercentagesAux = 0
                    for ifid in infectedID:
                        dist = int(math.dist(offsets[i][j],offsets[i][ifid]))
                        if (dist < infectingDistance):
                            infectionPercentages[i][j] = infectionPercentages[i-1][j] + infectingRate
                            rPercentagesAux += infectingRate
                            colors[i][j] = "black"
                    if (infectionPercentages[i][j] >= 100):
                        infectTaxi(i,j)
        hourloop += 1
        bar.next()

# Save infected by distirct at a given frame
with IncrementalBar(menus.infectedbydistricttext, max= len(offsets[0]), suffix = menus.suffix) as bar:
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
        bar.next()
        
                    
conn.close()

# Write to files

# Gets general directory to file
folder = os.getcwd() + subfolder

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

# Create File with offsets and infections
with open(folder + 'simulateInfection.csv', 'w', newline='') as sif:
    with IncrementalBar(menus.savesimulateinfectiontext, max= len(offsets), suffix = menus.suffix) as bar:
        sifw = csv.writer(sif)
        for rf, rc in zip(offsets,colors):
            row = []
            for cf, cc in zip(rf,rc):
                if (cf != [0,0]):
                    row.append(str(cf[0]) + " " + str(cf[1]) + " " + cc)
            sifw.writerow(row)
            bar.next()

# Create file with number of infected an file with R
with open(folder + 'infections.csv', 'w', newline='') as nif:

    nifw = csv.writer(nif)
    nifw.writerow([nInfected[0]])

    with IncrementalBar(menus.saveNInfectedtext, max= len(nInfected)-1, suffix = menus.suffix) as bar:
        for i in range(1,len(nInfected)):
            nifw.writerow([nInfected[i]])
            bar.next()

with open(folder + 'rvalues.csv', 'w', newline='') as rv:

    rvw = csv.writer(rv)

    with IncrementalBar(menus.saveRtext, max= len(r), suffix = menus.suffix) as bar:
        for i in range(0,len(r)):
            rvw.writerow([r[i]])
            bar.next()

# Create file with new infections by dristrict 
with open(folder + 'infectionsByDistrict.csv', 'w', newline='') as isbdf:
    with IncrementalBar(menus.saveInfectedByDistricttext, max= len(infectedByDistrict), suffix = menus.suffix) as bar:
        isbdfw = csv.writer(isbdf)
        for row in infectedByDistrict:
            isbdfw.writerow(row)
            bar.next()

# Create file with infected by district
with open(folder + 'infectedByDistrict.csv', 'w', newline='') as idbdf:
    with IncrementalBar(menus.saveInfectedByDistricttext, max= len(infectedByDistrict), suffix = menus.suffix) as bar:
        idbdfw = csv.writer(idbdf)
        for row in infectedByDistrict:
            idbdfw.writerow(row)
            bar.next()

# Print total run time
print(menus.enlapsedtimetext + str(datetime.timedelta(seconds=(time.time() - start_time))))
print("Files saved in: " + folder)
