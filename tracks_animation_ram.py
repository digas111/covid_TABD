import numpy as np
import matplotlib.pyplot as plt
import psycopg2
import math
from matplotlib.animation import FuncAnimation
import datetime
import csv
from postgis import Polygon,MultiPolygon
from postgis.psycopg import register
from textwrap import wrap

ts_i = 1570665600

xs_min, xs_max, ys_min, ys_max = -120000, 163000, -310000, 285000
width_in_inches = (xs_max-xs_min)/0.0254*1.1
height_in_inches = (ys_max-ys_min)/0.0254*1.1

nI = []
rAux = 1
timeHour = 0

# i=frame
def animate(i, x, nInfected, line, line2, rValues, animationsIndexsHour):

    global offsets
    global colors
    global nInfectedByDistrict
    global maxVDistrict
    global rAux
    global timeHour


    #------------------ Gráfico de Portugal -----------------
    axPortugal.set_title(datetime.datetime.utcfromtimestamp(ts_i+i*10))
    scatPortugal.set_offsets(offsets[i])
    scatPortugal.set_color(colors[i])

    
    #------------------ Gráfico de Porto -----------------
    
    scatPorto.set_offsets(offsets[i])
    scatPorto.set_color(colors[i])
    
    
    #------------------ Gráfico de Lisboa -----------------

    scatLisboa.set_offsets(offsets[i])
    scatLisboa.set_color(colors[i])


    #------------------ Gráfico de infetados/distrito -----------------
    
    for j , b in enumerate(barplot):
        if (nInfectedByDistrict[i][j] > 0 and nInfectedByDistrict[i][j] != nInfectedByDistrict[i-1][j]):
            if nInfectedByDistrict[i][j] > maxVDistrict:
                maxVDistrict = nInfectedByDistrict[i][j]
                axInfectedDistrict.set_xlim([0,maxVDistrict+1])
            for txt in axInfectedDistrict.texts:
                if  txt.get_position()[1] == j:
                    txt.remove()
            b.set_width(nInfectedByDistrict[i][j])
            axInfectedDistrict.text(nInfectedByDistrict[i][j], j , " " + str(nInfectedByDistrict[i][j]) + " (" + "{:.2f}".format(nInfectedByDistrict[i][j]/1660 * 100) + "%)" , va = "center", fontweight = 'bold')
    

    #------------------ Gráfico de curva de infeção -----------------

    axInfections.set_title("Curva de infeção: " + str(nInfected[i]) , fontsize = 'medium')
    line.set_data(x[:i], nInfected[:i])
    line.axes.axis([0, x[i]+1, 0, nInfected[i]+1])
    
    #------------------ Gráfico do R -----------------
    if(timeHour == 360 or timeHour == 0):
        print("timehour: " + str(timeHour) + " animationsIndexsHour[:rAux]:  " + str(animationsIndexsHour[:rAux]) + " rValues[:rAux] " + str(rValues[:rAux]) )
        timeHour = 0
        line2.set_data(animationsIndexsHour[:rAux], rValues[:rAux])
        line2.axes.axis([0, animationsIndexsHour[rAux]+1, 0, rValues[rAux]+1])
        rAux +=1
    
    timeHour+=1


scale=1/3000000
conn = psycopg2.connect("dbname=tabd user=postgres password=11223344Ab")
register(conn)


mapsPortugal = "E:\TrabalhoManel\Fac\TABD\covid_TABD\maps\portugal.csv"
mapsPorto = "E:\TrabalhoManel\Fac\TABD\covid_TABD\maps\porto.csv"
mapsLisboa = "E:\TrabalhoManel\Fac\TABD\covid_TABD\maps\lisboa.csv"

fig = plt.figure(figsize=(width_in_inches*scale*4, height_in_inches*scale), constrained_layout = True )
gs = fig.add_gridspec(2,4)


#-------------------------------------PLOT DE PORTUGAL----------------------------------------------------------------------

#axPortugal = fig.add_subplot(1,4,1)
axPortugal = fig.add_subplot(gs[:,0])
axPortugal.axis('off')
axPortugal.set(xlim=(xs_min, xs_max), ylim=(ys_min, ys_max))


with open(mapsPortugal, 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        xs , ys = [],[]
        for column in row:
            x,y = column.split()
            xs.append(float(x))
            ys.append(float(y))
        axPortugal.plot(xs,ys,color='black',lw='0.2')

#------------------------------PLOT DO PORTO--------------------------------------------------------------------------------------------

#axPorto = fig.add_subplot(2,4,2)
axPorto = fig.add_subplot(gs[0,1])
axPorto.axis('off')
axPorto.set_title("Concelhos: PORTO, VILA NOVA DE GAIA, MATOSINHOS, MAIA", fontsize = 'medium', y=-0.10)

with open(mapsPorto, 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        xs , ys = [],[]
        for column in row:
            x,y = column.split()
            xs.append(float(x))
            ys.append(float(y))
        axPorto.plot(xs,ys,color='black',lw='0.2')

#----------------------------------PLOT DE LISBOA----------------------------------------------------------------------------------------------

#axLisboa = fig.add_subplot(2,4,6)
axLisboa = fig.add_subplot(gs[1,1])
axLisboa.axis('off')
axLisboa.set_title("\n".join(wrap("Concelhos: LISBOA, OEIRAS, CASCAIS, SINTRA, AMADORA, ODIVELAS, LOURES, ALMADA, SEIXAL, MOITA")), fontsize = 'small', y=-0.10)

with open(mapsLisboa, 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        xs , ys = [],[]
        for column in row:
            x,y = column.split()
            xs.append(float(x))
            ys.append(float(y))
        axLisboa.plot(xs,ys,color='black',lw='0.2')


#----------------------------------PLOT DE infetados por distrito-----------------------------------------------------------------------------------

#axInfectedDistrict = fig.add_subplot(2,3,6)
axInfectedDistrict = fig.add_subplot(gs[1,2:])
labels = ["AVEIRO", "BEJA" ,"BRAGA", "BRAGANÇA", "CASTELO BRANCO", "COIMBRA", "ÉVORA", "FARO", "GUARDA", "LEIRIA", "LISBOA" , "PORTALEGRE" , "PORTO" , "SANTARÉM", "SETÚBAL" , "V.CASTELO" ,"VILA REAL" , "VISEU" ]
values = [0]*len(labels)

y_pos = np.arange(len(labels))

barplot = axInfectedDistrict.barh(y_pos,values, align='center')
axInfectedDistrict.set_yticks(y_pos)
axInfectedDistrict.set_yticklabels(labels, fontsize = 'x-small')
axInfectedDistrict.invert_yaxis()
axInfectedDistrict.set_xlabel("Nº infetados")
axInfectedDistrict.set_title("Infetados/Distrito", fontsize = 'small')

maxVDistrict = 0

#-----------------------------------PLOT DA CURVA DE INFEÇÃO--------------------------------------------------------------------------------

#axInfections = fig.add_subplot(4,4,3)
axInfections = fig.add_subplot(gs[0,2])
axInfections.set_xlabel('Tempo em seg', fontsize = 'small', ma = "left")
axInfections.set_ylabel('Infetados')
axInfections.set_title("Curva de infeção", fontsize = 'medium')



#-----------------------------------PLOT DO R----------------------------------------------------------------------------------------------

#axR = fig.add_subplot(4,4,8)
axR = fig.add_subplot(gs[0,3])
axR.set_xlabel('Tempo em seg', fontsize = 'small', ma = 'left')
axR.set_ylabel('R')
axR.set_title("Gráfico do R", fontsize = 'medium')

#-----------------------------ABERTURA DE FICHEIROS E CHAMADA DE ANIMAÇÃO----------------------------------------------------------------------------------------------

"""
simulateInfectionCSV = "data/porto&lisboa/simulateInfection.csv"
infectedByDistrictCSV = "data/porto&lisboa/infectedByDistrict.csv"
nInfectedCSV = "data/porto&lisboa/infections.csv"
"""

simulateInfectionCSV = "E:\TrabalhoManel\Fac\TABD\covid_TABD\data\PortoLisboa\simulateInfection.csv"
infectedByDistrictCSV = "E:\TrabalhoManel\Fac\TABD\covid_TABD\data\PortoLisboa\infectedByDistrict.csv"
nInfectedCSV = "E:\TrabalhoManel\Fac\TABD\covid_TABD\data\PortoLisboa\infections.csv"
rValuesCSV = "E:/TrabalhoManel/Fac/TABD/covid_TABD/data/PortoLisboa/rvalues.csv"


offsets = []
colors = []
nInfected = []
nInfectedByDistrict = []
rValues = []

with open(simulateInfectionCSV, 'r') as csvFile, open(infectedByDistrictCSV, 'r') as csvFile2, open(nInfectedCSV, 'r') as csvFile3, open(rValuesCSV, 'r') as csvFile4:
    
    reader = csv.reader(csvFile)
    reader2 = csv.reader(csvFile2)
    reader3 = csv.reader(csvFile3)
    reader4 = csv.reader(csvFile4)

    for row in reader:
        offsetsaux = []
        coloraux = []
        for column in row:
            x,y,color = column.split()
            x = float(x)
            y = float(y)
            offsetsaux.append([x,y])
            coloraux.append(color)

        offsets.append(offsetsaux)
        colors.append(coloraux)

    for row in reader2:
        nInfectedByDistrictaux = []
        for column in row:
            nInfectedByDistrictaux.append(int(column))

        nInfectedByDistrict.append(nInfectedByDistrictaux)
    
    for row in reader3:
        nInfected.append(int(row[0]))       

    for row in reader4:
        rValues.append(float(row[0]))

x,y = [],[]
for i in offsets[0]:
    x.append(i[0])
    y.append(i[1])

    

scatPortugal = axPortugal.scatter(x,y,s=2,color='orange')
scatPorto = axPorto.scatter(x,y,s=2,color='orange')
scatLisboa = axLisboa.scatter(x,y,s=2,color='orange')

animationIndexs = [n for n in range(0,len(nInfected))]

animationsIndexsHour = [n for n in range(0,8640-360,360)]

line, = axInfections.plot(animationIndexs, nInfected)

line2, = axR.plot(animationsIndexsHour,rValues)

anim = FuncAnimation(fig, animate, interval=10, frames=8640, fargs=[animationIndexs, nInfected, line, line2, rValues, animationsIndexsHour], repeat = False, blit = False)

plt.draw()
plt.show()
