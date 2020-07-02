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
#axPorto.set(xlim=(-54900,21600), ylim = (148000, 200500))
axPorto.set_title("Concelhos: PORTO, VILA NOVA DE GAIA, MATOSINHOS, MAIA", fontsize = 'medium', y=-0.10)


axLisboa = fig.add_subplot(2,3,5)
axLisboa.axis('off')
#axLisboa.set(xlim=(-118900,-56100), ylim=(-109900,-38300))
axLisboa.set_title("\n".join(wrap("Concelhos: LISBOA, OEIRAS, CASCAIS, SINTRA, AMADORA, ODIVELAS, LOURES, ALMADA, SEIXAL, MOITA")), fontsize = 'small', y=-0.10)



cursor_psql = conn.cursor()


#-------------------------------------PLOT DE PORTUGAL----------------------------------------------------------------------

sql = "select distrito,st_union(proj_boundary) from cont_aad_caop2018 group by distrito"

cursor_psql.execute(sql)
results = cursor_psql.fetchall()
xs , ys = [],[]
for row in results:
    geom = row[1]
    if type(geom) is MultiPolygon:
        for pol in geom:
            xys = pol[0].coords
            xs, ys = [],[]
            for (x,y) in xys:
                xs.append(x)
                ys.append(y)
            axPortugal.plot(xs,ys,color='black',lw='0.2')
    if type(geom) is Polygon:
        xys = geom[0].coords
        xs, ys = [],[]
        for (x,y) in xys:
            xs.append(x)
            ys.append(y)
        axPortugal.plot(xs,ys,color='black',lw='0.2')


#------------------------------PLOT DO PORTO--------------------------------------------------------------------------------------------


sql = "select concelho, st_union(proj_boundary) from cont_aad_caop2018 where concelho = 'PORTO' or concelho = 'VILA NOVA DE GAIA' or concelho = 'MATOSINHOS' or concelho = 'MAIA' or concelho = 'VALONGO' or concelho = 'GONDOMAR' group by concelho"

# select distrito, st_union(proj_boundary) from cont_aad_caop2018 where concelho = 'PORTO' or concelho = 'VILA NOVA DE GAIA' or concelho = 'MATOSINHOS' or concelho = 'MAIA group by distrito'

cursor_psql.execute(sql)
results = cursor_psql.fetchall()
xs , ys = [],[]
for row in results:
    geom = row[1]
    if type(geom) is MultiPolygon:
        for pol in geom:
            xys = pol[0].coords
            xs, ys = [],[]
            for (x,y) in xys:
                xs.append(x)
                ys.append(y)
            axPorto.plot(xs,ys,color='black',lw='0.2')
    if type(geom) is Polygon:
        xys = geom[0].coords
        xs, ys = [],[]
        for (x,y) in xys:
            xs.append(x)
            ys.append(y)
        axPorto.plot(xs,ys,color='black',lw='0.2')


#----------------------------------PLOT DE LISBOA----------------------------------------------------------------------------------------------

sql = "select concelho, st_union(proj_boundary) from cont_aad_caop2018 where concelho = 'LISBOA' or concelho = 'OEIRAS' or concelho = 'CASCAIS' or concelho = 'SINTRA' or concelho = 'AMADORA' or concelho = 'ODIVELAS' or concelho = 'LOURES' or concelho = 'ALMADA' or concelho = 'SEIXAL' or concelho = 'MOITA' and (distrito = 'LISBOA' or distrito = 'SET┌BAL') group by concelho"

# select distrito, st_union(proj_boundary) from cont_aad_caop2018 where concelho = 'LISBOA' or concelho = 'OEIRAS' or concelho = 'CASCAIS' or concelho = 'SINTRA' or concelho = 'AMADORA' or concelho = 'ODIVELAS' or concelho = 'LOURES' or concelho = 'ALMADA' or concelho = 'SEIXAL' or concelho = 'MOITA' and (distrito = 'LISBOA' or distrito = 'SET┌BAL') group by distrito

cursor_psql.execute(sql)
results = cursor_psql.fetchall()
xs , ys = [],[]
for row in results:
    geom = row[1]
    if type(geom) is MultiPolygon:
        for pol in geom:
            xys = pol[0].coords
            xs, ys = [],[]
            for (x,y) in xys:
                xs.append(x)
                ys.append(y)
            axLisboa.plot(xs,ys,color='black',lw='0.2')
    if type(geom) is Polygon:
        xys = geom[0].coords
        xs, ys = [],[]
        for (x,y) in xys:
            xs.append(x)
            ys.append(y)
        axLisboa.plot(xs,ys,color='black',lw='0.2')


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
axInfections.axis('on')
axInfections.set_xlabel('Tempo em seg', fontsize = 'small', ma = "left")
axInfections.set_ylabel('Infetados')
axInfections.set_title("Curva de infeção", fontsize = 'medium')

#-----------------------------ABERTURA DE FICHEIROS E CHAMADA DE ANIMAÇÃO----------------------------------------------------------------------------------------------

simulateInfectionCSV = "E:\TrabalhoManel\Fac\TABD\covid_TABD\simulateInfection.csv"
infectedByDistrictCSV = "E:\TrabalhoManel\Fac\TABD\covid_TABD\infectedByDistrict.csv"
nInfectedCSV = "E:\TrabalhoManel\Fac\TABD\covid_TABD\infections.csv"

with open(simulateInfectionCSV, 'r') as csvFile, open(infectedByDistrictCSV, 'r') as csvFile2, open(nInfectedCSV, 'r') as csvFile3:
    reader = csv.reader(csvFile)

    line = next(reader)

    x,y = [],[]
    for i in line:
        if (i[0] != 0 and i[1] != 0):
            x.append(i[0])
            y.append(i[1])

    scatPortugal = axPortugal.scatter(x,y,s=2,color='orange')
    scatPorto = axPorto.scatter(x,y,s=2,color='orange')
    scatLisboa = axLisboa.scatter(x,y,s=2,color='orange')

    reader2 = csv.reader(csvFile2)

    reader3 = csv.reader(csvFile3)
    
    anim = FuncAnimation(fig, animate, interval=1, frames=8640-1, repeat = False)

    plt.draw()
    plt.show()
