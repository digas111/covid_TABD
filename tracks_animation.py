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

# i=frame
def animate(i):
    global reader
    global reader2
    global reader3

    axInfectedDistrict.clear()
    axInfections.clear()
    axPortugal.set_title(datetime.datetime.utcfromtimestamp(ts_i+i*10))

    offsets = []
    colors = []

    line = next(reader)
    for row in line:
        x,y,color = row.split()
        x = float(x)
        y = float(y)
        offsets.append([x,y])
        colors.append(color)
    
    infectedD = []
    axInfectedDistrict.set_title("Infetados/Distrito", fontsize = 'small')
    axInfectedDistrict.set_yticks(y_pos)
    axInfectedDistrict.set_yticklabels(labels, fontsize = 'x-small')
    axInfectedDistrict.invert_yaxis()
    axInfectedDistrict.set_xlabel("Nº infetados")

    line = next(reader2)
    for column in line:
        x=int(column)
        infectedD.append(x)

    axInfectedDistrict.barh(y_pos, infectedD, align='center')
    for i , v in enumerate(infectedD):
        axInfectedDistrict.text(v, i , " " + str(v), va = "center", fontweight = 'bold')
    
    row = next(reader3)
    for column in row:
        x=int(column)
        nI.append(x)


    axInfections.set_xlabel('Tempo em seg', fontsize = 'small', ma = "left")
    axInfections.set_ylabel('Infetados')
    axInfections.set_title("Curva de infeção", fontsize = 'medium') 
    axInfections.plot(nI)

    # axInfections.set_xdata(i)
    # axInfections.set_ydata(nI)

    scatPortugal.set_offsets(offsets)
    scatPortugal.set_color(colors)
   
    scatPorto.set_offsets(offsets)
    scatPorto.set_color(colors)
    
    scatLisboa.set_offsets(offsets)
    scatLisboa.set_color(colors)

    

scale=1/3000000
conn = psycopg2.connect("dbname=tabd user=postgres password=11223344Ab")
register(conn)


fig = plt.figure(figsize=(width_in_inches*scale*4, height_in_inches*scale*1.05), )

axPortugal = fig.add_subplot(1,3,1)
axPortugal.axis('off')
axPortugal.set(xlim=(xs_min, xs_max), ylim=(ys_min, ys_max))

axPorto = fig.add_subplot(2,3,2)
axPorto.axis('off')
axPorto.set_title("Concelhos: PORTO, VILA NOVA DE GAIA, MATOSINHOS, MAIA", fontsize = 'medium', y=-0.10)


axLisboa = fig.add_subplot(2,3,5)
axLisboa.axis('off')
axLisboa.set_title("\n".join(wrap("Concelhos: LISBOA, OEIRAS, CASCAIS, SINTRA, AMADORA, ODIVELAS, LOURES, ALMADA, SEIXAL, MOITA")), fontsize = 'small', y=-0.10)

#-------------------------------------PLOT DE PORTUGAL----------------------------------------------------------------------

with open('E:\TrabalhoManel\Fac\TABD\covid_TABD\maps\portugal.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        xs , ys = [],[]
        for column in row:
            x,y = column.split()
            xs.append(float(x))
            ys.append(float(y))
        axPortugal.plot(xs,ys,color='black',lw='0.2')

#------------------------------PLOT DO PORTO--------------------------------------------------------------------------------------------

with open('E:\TrabalhoManel\Fac\TABD\covid_TABD\maps\porto.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        xs , ys = [],[]
        for column in row:
            x,y = column.split()
            xs.append(float(x))
            ys.append(float(y))
        axPorto.plot(xs,ys,color='black',lw='0.2')

#----------------------------------PLOT DE LISBOA----------------------------------------------------------------------------------------------

with open('E:\TrabalhoManel\Fac\TABD\covid_TABD\maps\lisboa.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        xs , ys = [],[]
        for column in row:
            x,y = column.split()
            xs.append(float(x))
            ys.append(float(y))
        axLisboa.plot(xs,ys,color='black',lw='0.2')

#----------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------PLOT DE Grafico de Barras----------------------------------------------------------------------------------------------


# numero de infetados por distrito (barras)
axInfectedDistrict = fig.add_subplot(2,3,6)
axInfectedDistrict.axis('on')
labels = ["AVEIRO", "BEJA" ,"BRAGA", "BRAGANÇA", "CASTELO BRANCO", "COIMBRA", "ÉVORA", "FARO", "GUARDA", "LEIRIA", "LISBOA" , "PORTALEGRE" , "PORTO" , "SANTARÉM", "SETÚBAL" , "V.CASTELO" ,"VILA REAL" , "VISEU" ]
values = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

y_pos = np.arange(len(labels))

axInfectedDistrict.barh(y_pos, values, align='center')
axInfectedDistrict.set_yticks(y_pos)
axInfectedDistrict.set_yticklabels(labels, fontsize = 'x-small')
axInfectedDistrict.invert_yaxis()
axInfectedDistrict.set_xlabel("Nº infetados")
axInfectedDistrict.set_title("Infetados/Distrito", fontsize = 'small')

for i , v in enumerate(values):
    axInfectedDistrict.text(v, i , " " + str(v), va = "center", fontweight = 'bold')

#-----------------------------------PLOT DA CURVA----------------------------------------------------------------------------------------------

axInfections = fig.add_subplot(2,3,3)
# line, = ax.plot([0,1],[0,0])
axInfections.set_xlabel('Tempo em seg', fontsize = 'small', ma = "left")
axInfections.set_ylabel('Infetados')
axInfections.set_title("Curva de infeção", fontsize = 'medium')

#-----------------------------ABERTURA DE FICHEIROS E CHAMADA DE ANIMAÇÃO----------------------------------------------------------------------------------------------


#simulateInfectionCSV = "data/simulateInfection.csv"
#infectedByDistrictCSV = "data/infectedByDistrict.csv"
#nInfectedCSV = "data/infections.csv"


simulateInfectionCSV = "E:\TrabalhoManel\Fac\TABD\covid_TABD\data\porto&lisboa\simulateInfection.csv"
infectedByDistrictCSV = "E:\TrabalhoManel\Fac\TABD\covid_TABD\data\porto&lisboa\infectedByDistrict.csv"
nInfectedCSV = "E:\TrabalhoManel\Fac\TABD\covid_TABD\data\porto&lisboa\infections.csv"

with open(simulateInfectionCSV, 'r') as csvFile, open(infectedByDistrictCSV, 'r') as csvFile2, open(nInfectedCSV, 'r') as csvFile3:
    
    reader = csv.reader(csvFile)
    reader2 = csv.reader(csvFile2)
    reader3 = csv.reader(csvFile3)

    line = next(reader)

    x,y = [],[]
    for i in line:
        x.append(i[0])
        y.append(i[1])

    scatPortugal = axPortugal.scatter(x,y,s=2,color='orange')
    scatPorto = axPorto.scatter(x,y,s=2,color='orange')
    scatLisboa = axLisboa.scatter(x,y,s=2,color='orange')

    
    
    anim = FuncAnimation(fig, animate, interval=10, frames=8640-1, repeat = False)

    plt.draw()
    plt.show()
