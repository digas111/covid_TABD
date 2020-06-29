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

xs_min, xs_max, ys_min, ys_max = -120000, 165000, -310000, 285000
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


# deletes all taxis in (0,0) as they are inactive
def cleanInactive(m):
    n = []
    for i in m:
        if (i[0] != 0 and i[1] != 0):
            n.append(i)
    return n



# i=frame
def animate(i):

    offsets = []
    colors  = []
    with open('E:\TrabalhoManel\Fac\TABD\covid_TABD\simulateInfection.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        frame=0
        for line in reader:  
            if(frame == i):
                for item in line:
                    x,y,color = item.split()
                    x = float(x)
                    y = float(y)
                    offsets.append([x,y])
                    colors.append(color)
                break
            frame+=1   

  
    ax.set_title(datetime.datetime.utcfromtimestamp(ts_i+i*10))

    scat.set_offsets(offsets)
    scat.set_color(colors)

    #ax.set(xlim=(-120000+i*10, 165000-i*100), ylim=(-310000+i*100*2.09, 285000-i*10*2.09))
    #ax.set(xlim=(-120000+i*xe, 165000-i*xd), ylim=(-310000+i*yb, 285000-i*yc))

    
    

scale=1/3000000
conn = psycopg2.connect("dbname=tabd user=postgres password=11223344Ab")
register(conn)

# xs_min, xs_max, ys_min, ys_max = -120000, 165000, -310000, 285000
# width_in_inches = (xs_max-xs_min)/0.0254*1.1
# height_in_inches = (ys_max-ys_min)/0.0254*1.1

fig, ax = plt.subplots(figsize=(width_in_inches*scale, height_in_inches*scale))
ax.axis('off')
ax.set(xlim=(xs_min, xs_max), ylim=(ys_min, ys_max))

cursor_psql = conn.cursor()

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
            ax.plot(xs,ys,color='black',lw='0.2')
    if type(geom) is Polygon:
        xys = geom[0].coords
        xs, ys = [],[]
        for (x,y) in xys:
            xs.append(x)
            ys.append(y)
        ax.plot(xs,ys,color='black',lw='0.2')

offsets = []
colors = []
nInfected = []
"""
with open('E:\TrabalhoManel\Fac\TABD\covid_TABD\simulateInfection.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        l = []
        colorsIt = []
        nInfected.append(row[0])
        for j in range(1,len(row)):
            x,y,color = row[j].split()
            x = float(x)
            y = float(y)
            colorsIt.append(color)
            l.append([x,y])
        offsets.append(l)
        colors.append(colorsIt)


#print(nInfected)

x,y = [],[]
for i in offsets[0]:
    if (i[0] != 0 and i[1] != 0):
        x.append(i[0])
        y.append(i[1])
"""





x,y = [],[]
colors  = []
with open('E:\TrabalhoManel\Fac\TABD\covid_TABD\simulateInfection.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    frame=0
    for line in reader: 
        print(frame) 
        if(frame == 0):
            for item in line:
                x,y,color = item.split()
                x = float(x)
                y = float(y)
                x.append(x)
                y.append(y)
                colors.append(color)
            break
        frame+=1



scat = ax.scatter(x,y,s=2,color='orange')
#100 fps

print("ANTES DA FUNCANIMATION")


anim = FuncAnimation(fig, animate, interval=10, frames=8640-1, repeat = False)

print("DEPOIS DA FUNCANIMATION")
#anim = FuncAnimation(fig, animate, interval=10, frames=len(offsets)-1, fargs=, repeat = False)



plt.draw()
print("DEPOIS DO DRAW")
plt.show()
print("DEPOIS DO SHPW")
