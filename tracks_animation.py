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


fig = plt.figure(figsize=(width_in_inches*scale*4, height_in_inches*scale*1.05))

axPortugal = fig.add_subplot(1,3,1)
axPortugal.axis('on')
axPortugal.set(xlim=(xs_min, xs_max), ylim=(ys_min, ys_max))

axPorto = fig.add_subplot(2,3,2)
axPorto.axis('on')
#axPorto.set(xlim=(-54900,21600), ylim = (148000, 200500))

axLisboa = fig.add_subplot(2,3,5)
axLisboa.axis('on')
#axLisboa.set(xlim=(-118900,-56100), ylim=(-109900,-38300))


cursor_psql = conn.cursor()


#-------------------------------------PLOT DE PORTUGAL---------------------

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


#------------------------------PLOT DO PORTO----------------------


sql = "select distrito, st_union(proj_boundary) from cont_aad_caop2018 where concelho = 'PORTO' or concelho = 'VILA NOVA DE GAIA' or concelho = 'MATOSINHOS' or concelho = 'MAIA' group by distrito"

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


#----------------------------------PLOT DE LISBOA------------------------
sql = "select distrito, st_union(proj_boundary) from cont_aad_caop2018 where concelho = 'LISBOA' or concelho = 'OEIRAS' or concelho = 'CASCAIS' or concelho = 'SINTRA' or concelho = 'AMADORA' or concelho = 'ODIVELAS' or concelho = 'LOURES' or concelho = 'ALMADA' or concelho = 'SEIXAL' or concelho = 'MOITA' and (distrito = 'LISBOA' or distrito = 'SET┌BAL') group by distrito"

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

offsets = []
colors = []

# with open('simulateInfection.csv', 'r') as csvFile:
#     reader = csv.reader(csvFile)
#     for row in reader:
#         l = []
#         colorsIt = []
#         for j in range(1,len(row)):
#             x,y,color = row[j].split()
#             x = float(x)
#             y = float(y)
#             colorsIt.append(color)
#             l.append([x,y])
#         offsets.append(l)
#         colors.append(colorsIt)


#print(nInfected)

with open('simulateInfection.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)

    line = next(reader)

    x,y = [],[]
    for i in line:
        if (i[0] != 0 and i[1] != 0):
            x.append(i[0])
            y.append(i[1])

    scat = axPortugal.scatter(x,y,s=2,color='orange')
    #100 fps



    anim = FuncAnimation(fig, animate, interval=10, frames=8640-1, repeat = False)


    plt.draw()
    plt.show()
