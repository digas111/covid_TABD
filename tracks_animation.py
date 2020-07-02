# /Applications/Postgres.app/Contents/Versions/12/bin/psql -p5432 "postgres"

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


portoxEsq = -56510
portoxDir = -22614
portoyCim = 182294
portoyBai = 144468
portoDuration = 60


def zoom(ci,cf,durationSeconds):
    df = durationSeconds*100
    return abs(cf-ci)/df


xe = zoom(xs_min,portoxEsq,portoDuration)
xd = zoom(xs_max,portoxDir,portoDuration)
yb = zoom(ys_min,portoyBai,portoDuration)
yc = zoom(ys_max,portoyCim,portoDuration)


# i=frame
def animate(i):
    global reader

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


    scat.set_offsets(offsets)
    scat.set_color(colors)

    

scale=1/3000000
conn = psycopg2.connect("dbname=postgres user=postgres")
register(conn)


fig = plt.figure(figsize=(width_in_inches*scale*4, height_in_inches*scale*1.05), )

axPortugal = fig.add_subplot(1,3,1)
axPortugal.axis('off')
axPortugal.set(xlim=(xs_min, xs_max), ylim=(ys_min, ys_max))

axPorto = fig.add_subplot(2,3,2)
axPorto.axis('off')
#axPorto.set(xlim=(-54900,21600), ylim = (148000, 200500))
axPorto.set_title("Concelhos: PORTO, VILA NOVA DE GAIA, MATOSINHOS, MAIA", fontsize = 'medium', y=-0.10)


axLisboa = fig.add_subplot(2,3,5)
axLisboa.axis('off')
#axLisboa.set(xlim=(-118900,-56100), ylim=(-109900,-38300))
axLisboa.set_title("\n".join(wrap("Concelhos: LISBOA, OEIRAS, CASCAIS, SINTRA, AMADORA, ODIVELAS, LOURES, ALMADA, SEIXAL, MOITA")), fontsize = 'small', y=-0.10)

# numero de infeçoes/tempo (curva)
axInfections = fig.add_subplot(2,3,3)
axInfections.axis('on')
axInfections.set_xlabel('Tempo em seg', fontsize = 'small', ma = "left")
axInfections.set_ylabel('Infetados')
axInfections.set_title("Curva de infeção", fontsize = 'medium')

# numero de infetados por distrito (barras)
axInfectedDistrict = fig.add_subplot(2,3,6)
axInfectedDistrict.axis('on')
labels = ["AVEIRO", "BEJA" ,"BRAGA", "BRAGANÇA", "CASTELO BRANCO", "COIMBRA", "ÉVORA", "FARO", "GUARDA", "LEIRIA", "LISBOA" , "PORTALEGRE" , "PORTO" , "SANTARÉM", "SETÚBAL" , "V.CASTELO" ,"VILA REAL" , "VISEU" ]
values = [1,2,3,4,5,6,7,8,9, 10, 11, 12, 13 ,14 ,15, 16, 17, 18]

y_pos = np.arange(len(labels))

axInfectedDistrict.barh(y_pos, values, align='center')
axInfectedDistrict.set_yticks(y_pos)
axInfectedDistrict.set_yticklabels(labels, fontsize = 'x-small')
axInfectedDistrict.invert_yaxis()
axInfectedDistrict.set_xlabel("Nº infetados")
axInfectedDistrict.set_title("Infetados/Distrito", fontsize = 'small')
axInfectedDistrict.set(xlim=(0, 20))

for i , v in enumerate(values):
    axInfectedDistrict.text(v, i , " " + str(v), va = "center", fontweight = 'bold')




cursor_psql = conn.cursor()


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

with open('data/simulateInfection.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)

    line = next(reader)

    x,y = [],[]
    for i in line:
        if (i[0] != 0 and i[1] != 0):
            x.append(i[0])
            y.append(i[1])

    scat = axPortugal.scatter(x,y,s=2,color='orange')
    #100 fps


    anim = FuncAnimation(fig, animate, interval=5, frames=8640-1, repeat = False)


    plt.draw()
    plt.show()
