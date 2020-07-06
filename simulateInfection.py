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

#Save inicial time to print
start_time = 0

subfolder = ""

##########

infectingDistance = 80
infectingRate = 20 #percentage by frame
ninfectedBeforeMask = 0

##########

conn = psycopg2.connect("dbname=postgres user=postgres")
register(conn)
cursor_psql = conn.cursor()

startingInfected = []
offsets = []
infectedID = []
infectionPercentages = []
colors = []
nInfected = []
infectedByDistrict = []
infectionsByDistrict = []



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

taxisPorto = [161, 238, 110, 978, 306, 723, 247, 664, 187, 958]
taxisLisboa= [1602, 836, 1285, 872, 1163, 815, 1180, 817, 1500, 1564]

#### FUNCTIONS ####

def infectTaxi(frame,row):

    global infectionPercentages
    global infectedID
    global nInfected
    global infectionsByDistrict
    global cursor_psql

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

### MENUS ###

title1 = "Primeiros infetados:"
menu1Items = ['Porto & Lisboa','Porto','Lisboa','Exit']

def print_menu1(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    x = w//2 - len(title1)//2
    y = h//3

    stdscr.addstr(y, x, title1)

    for idx, row in enumerate(menu1Items):
        x = w//2 - len(row)//2
        y = h//2 - len(menu1Items)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    
    stdscr.refresh()

def menu1(stdscr):

    global subfolder

    current_row_idx = 0

    print_menu1(stdscr, current_row_idx)
    
    while 1:
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu1Items)-1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10,13]:
            
            if (current_row_idx == 0):
                #Porto & Lisboa
                startingInfected.append(random.choice(taxisPorto))
                startingInfected.append(random.choice(taxisLisboa))
                subfolder = "porto&lisboa/"
                break
            elif (current_row_idx == 1):
                #Porto
                startingInfected.append(random.choice(taxisPorto))
                subfolder = "porto/"
                break
            elif (current_row_idx == 2):
                #Lisboa
                startingInfected.append(random.choice(taxisLisboa))
                subfolder = "lisboa/"
                break
            elif (current_row_idx == len(menu1Items)-1):
                exit(0)

        print_menu1(stdscr, current_row_idx)
        stdscr.refresh()



title2 = "Medidas de precaoção:"
menu2Items = ['Sim','Não','Exit']

def print_menu2(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    x = w//2 - len(title2)//2
    y = h//3

    stdscr.addstr(y, x, title2)

    for idx, row in enumerate(menu2Items):
        x = w//2 - len(row)//2
        y = h//2 - len(menu2Items)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    
    stdscr.refresh()

def menu2(stdscr):

    global subfolder

    current_row_idx = 0

    print_menu2(stdscr, current_row_idx)

    while 1:
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu2Items)-1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10,13]:

            if (current_row_idx == 0):
                #Sim
                print_menu3(stdscr)
                break
            
            elif (current_row_idx == 1):
                #Não
                break
           
            elif (current_row_idx == len(menu2Items)-1):
                exit(0)

        print_menu2(stdscr, current_row_idx)
        stdscr.refresh()


title3 = "Nº infected before taking measures:"

def print_menu3(stdscr):
    global ninfectedBeforeMask
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w//2 - len(title3)//2
    y = h//3

    curses.echo() 
    stdscr.addstr(y, x, title3)
    stdscr.refresh()
    x = w//2
    ninfectedBeforeMask = int(stdscr.getstr(y + 2, x, 20))


def mainMenu(stdscr):

    global subfolder

    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    menu1(stdscr)
    menu2(stdscr)

    
    # updateProgress(stdscr)

def run_simulation():

    global infectionPercentages
    global infectedID
    global nInfected
    global infectionsByDistrict
    global cursor_psql
    global subfolder
    global start_time

    start_time = time.time()

    with open('offsets3.csv', 'r') as csvFile:
        nrows = sum(1 for line in csv.reader(csvFile))
    
    #### Ler Offsets ####
    with open('offsets3.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        with IncrementalBar("Reading offsets", max= nrows, suffix = '%(percent)d%% | %(elapsed_td)s') as bar:
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
                bar.next()
            
    
    for taxi in startingInfected:
        infectTaxi(0,taxi)

    #### Simular propagação do virus ####
    with IncrementalBar("Simular propação do virus", max= len(offsets)-1, suffix = '%(percent)d%% | %(elapsed_td)s') as bar:
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
            bar.next()

    #### Infetados por distrito ####

    with IncrementalBar("Infetados por distrito", max= len(offsets[0]), suffix = '%(percent)d%% | %(elapsed_td)s') as bar:
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

    ##### WRITE TO FILES #####

    folder = os.getcwd()+"/data/" + subfolder

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
        with IncrementalBar("Saving simulateInfection", max= len(offsets), suffix = '%(percent)d%% | %(elapsed_td)s') as bar:
            sifw = csv.writer(sif)
            for rf, rc in zip(offsets,colors):
                row = []
                for cf, cc in zip(rf,rc):
                    if (cf != [0,0]):
                        row.append(str(cf[0]) + " " + str(cf[1]) + " " + cc)
                sifw.writerow(row)
                bar.next()

    # def writeNInfected():

    #### Create file with number of infected an file with R #### -> new thread

    
    with open(folder + 'infections.csv', 'w', newline='') as nif, open(folder + 'rvalues.csv', 'w', newline='') as rv:
        with IncrementalBar("Saving nº Infections and R values", max= len(nInfected), suffix = '%(percent)d%% | %(elapsed_td)s') as bar:

            nifw = csv.writer(nif)
            rvw = csv.writer(rv)

            nifw.writerow([nInfected[0]])
            rvw.writerow([0])
            bar.next()

            for i in range(1,len(nInfected)):
                nifw.writerow([nInfected[i]])
                rvw.writerow([(nInfected[i]-nInfected[i-1]) / nInfected[i-1]])
                bar.next()


    # def writeInfectionsByDistrict():

    #### Create file with new infections by dristrict #### -> new thread

    with open(folder + 'infectionsByDistrict.csv', 'w', newline='') as isbdf:
        with IncrementalBar("Saving infectionsByDistrict", max= len(infectedByDistrict), suffix = '%(percent)d%% | %(elapsed_td)s') as bar:
            isbdfw = csv.writer(isbdf)
            for row in infectedByDistrict:
                isbdfw.writerow(row)
                bar.next()

    # def writeInfectedByDistrict():

    #### Create file with infected by district #### -> new thread

    with open(folder + 'infectedByDistrict.csv', 'w', newline='') as idbdf:
        with IncrementalBar("Saving infectedByDistrict", max= len(infectedByDistrict), suffix = '%(percent)d%% | %(elapsed_td)s') as bar:
            idbdfw = csv.writer(idbdf)
            for row in infectedByDistrict:
                idbdfw.writerow(row)
                bar.next()

curses.wrapper(mainMenu)
run_simulation()

print("Ficheiros criados em: " + str(datetime.timedelta(seconds=(time.time() - start_time))))
