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
def animate(i, x, y, line):

    global offsets
    global colors
    global nInfectedByDistrict
    global maxVDistrict

    axPortugal.set_title(datetime.datetime.utcfromtimestamp(ts_i+i*10))

    for j , b in enumerate(barplot):
        if (nInfectedByDistrict[i][j] > 0 and nInfectedByDistrict[i][j] != nInfectedByDistrict[i-1][j]):
            if nInfectedByDistrict[i][j] > maxVDistrict:
                maxVDistrict = nInfectedByDistrict[i][j]
                axInfectedDistrict.set_xlim([0,maxVDistrict+1])
            for txt in axInfectedDistrict.texts:
                if txt.get_position()[0] == nInfectedByDistrict[i-1][j] and txt.get_position()[1] == j:
                    txt.remove()
            b.set_width(nInfectedByDistrict[i][j])
            axInfectedDistrict.text(nInfectedByDistrict[i][j], j , " " + str(nInfectedByDistrict[i][j]), va = "center", fontweight = 'bold')


    line.set_data(x[:i],y[:i])
    line.axes.axis([0, x[i]+1, 0, y[i]+1])
    

    scatPortugal.set_offsets(offsets[i])
    scatPortugal.set_color(colors[i])
   
    scatPorto.set_offsets(offsets[i])
    scatPorto.set_color(colors[i])
    
    scatLisboa.set_offsets(offsets[i])
    scatLisboa.set_color(colors[i])

    

scale=1/3000000
conn = psycopg2.connect("dbname=postgres user=postgres")
register(conn)


fig = plt.figure(figsize=(width_in_inches*scale*4, height_in_inches*scale), )

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

with open('maps/portugal.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        xs , ys = [],[]
        for column in row:
            x,y = column.split()
            xs.append(float(x))
            ys.append(float(y))
        axPortugal.plot(xs,ys,color='black',lw='0.2')

#------------------------------PLOT DO PORTO--------------------------------------------------------------------------------------------

with open('maps/porto.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        xs , ys = [],[]
        for column in row:
            x,y = column.split()
            xs.append(float(x))
            ys.append(float(y))
        axPorto.plot(xs,ys,color='black',lw='0.2')

#----------------------------------PLOT DE LISBOA----------------------------------------------------------------------------------------------

with open('maps/lisboa.csv', 'r') as csvFile:
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
# axInfectedDistrict.axis('on')
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

#-----------------------------------PLOT DA CURVA----------------------------------------------------------------------------------------------

axInfections = fig.add_subplot(4,3,3)
axInfections.set_xlabel('Tempo em seg', fontsize = 'small', ma = "left")
axInfections.set_ylabel('Infetados')
axInfections.set_title("Curva de infeção", fontsize = 'medium')

#-----------------------------ABERTURA DE FICHEIROS E CHAMADA DE ANIMAÇÃO----------------------------------------------------------------------------------------------

simulateInfectionCSV = "data/porto&lisboa/simulateInfection.csv"
infectedByDistrictCSV = "data/porto&lisboa/infectedByDistrict.csv"
nInfectedCSV = "data/porto&lisboa/infections.csv"



offsets = []
colors = []
nInfected = []
nInfectedByDistrict = []


with open(simulateInfectionCSV, 'r') as csvFile, open(infectedByDistrictCSV, 'r') as csvFile2, open(nInfectedCSV, 'r') as csvFile3:
    
    reader = csv.reader(csvFile)
    reader2 = csv.reader(csvFile2)
    reader3 = csv.reader(csvFile3)

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

x,y = [],[]
for i in offsets[0]:
    x.append(i[0])
    y.append(i[1])

    

scatPortugal = axPortugal.scatter(x,y,s=2,color='orange')
scatPorto = axPorto.scatter(x,y,s=2,color='orange')
scatLisboa = axLisboa.scatter(x,y,s=2,color='orange')

animationIndexs = [n for n in range(0,len(nInfected))]

line, = axInfections.plot(animationIndexs,nInfected)

anim = FuncAnimation(fig, animate, interval=10, frames=8640-1, fargs=[animationIndexs, nInfected, line], repeat = False)

plt.draw()
plt.show()
