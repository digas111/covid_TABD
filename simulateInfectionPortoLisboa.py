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

start_time = 0

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

subfolder = ""

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
menu1 = ['Porto & Lisboa','Porto','Lisboa','Exit']


title2 = "Utilização de máscara:"
menu2 = ['Sim','Não','Exit']

title3 = "Nº infetados antes de inicio de medidas:"

title4 = "Simulando..."


def print_menu1(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    x = w//2 - len(title1)//2
    y = h//3

    stdscr.addstr(y, x, title1)

    for idx, row in enumerate(menu1):
        x = w//2 - len(row)//2
        y = h//2 - len(menu1)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    
    stdscr.refresh()

def my_raw_input(stdscr, r, c, prompt_string):
    curses.echo() 
    stdscr.addstr(r, c, prompt_string)
    stdscr.refresh()
    input = stdscr.getstr(r + 1, c, 20)
    return input  #       ^^^^  reading input at next line  

def print_menu2(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    x = w//2 - len(title2)//2
    y = h//3

    stdscr.addstr(y, x, title2)

    for idx, row in enumerate(menu2):
        x = w//2 - len(row)//2
        y = h//2 - len(menu2)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    
    stdscr.refresh()

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

    for taxi in startingInfected:
        infectTaxi(0,taxi)

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

    

def main(stdscr):

    global subfolder

    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_row_idx = 0

    print_menu1(stdscr, current_row_idx)
    
    while 1:
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu1)-1:
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
            elif (current_row_idx == len(menu1)-1):
                exit(0)

        print_menu1(stdscr, current_row_idx)
        stdscr.refresh()


    print_menu2(stdscr, current_row_idx)

    while 1:
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu2)-1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10,13]:

            if (current_row_idx == 0):
                #Sim
                print_menu3(stdscr)
                break
            
            elif (current_row_idx == 1):
                #Não
                break
           
            elif (current_row_idx == len(menu2)-1):
                exit(0)

        print_menu2(stdscr, current_row_idx)
        stdscr.refresh()

    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w//2 - len(title4)//2
    y = h//2
    stdscr.addstr(y, x, title4)
    stdscr.refresh()


    run_simulation()

curses.wrapper(main)

print("Ficheiros criados em: " + str(datetime.timedelta(seconds=(time.time() - start_time))))
