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
    ax.set_title(datetime.datetime.utcfromtimestamp(ts_i+i*10))
    # scat.set_colors('red')

    # retira as coordenadas (0,0)
    # newOffsets = cleanInactive(offsets[i])
    # scat.set_offsets(newOffsets)

    scat.set_offsets(offsets[i])
    scat.set_color(colors[i])


    #ax.set(xlim=(-120000+i*10, 165000-i*100), ylim=(-310000+i*100*2.09, 285000-i*10*2.09))
    #ax.set(xlim=(-120000+i*xe, 165000-i*xd), ylim=(-310000+i*yb, 285000-i*yc))

    
    

scale=1/3000000
conn = psycopg2.connect("dbname=postgres user=postgres")
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

#with open('myoffsets2.csv', 'r') as csvFile:

with open('offsets3.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        l = []
        for j in row:
            x,y = j.split()
            x = float(x)
            y = float(y)
            l.append([x,y])
        offsets.append(l)

with open('simulateInfection.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        colorsIt = []
        for j in row:
            colorsIt.append(j)
        colors.append(colorsIt)




x,y = [],[]
for i in offsets[0]:
    if (i[0] != 0 and i[1] != 0):
        x.append(i[0])
        y.append(i[1])


scat = ax.scatter(x,y,s=2,color='orange')
#100 fps
anim = FuncAnimation(fig, animate, interval=10, frames=len(offsets)-1, repeat = False)
#anim = FuncAnimation(fig, animate, interval=10, frames=len(offsets)-1, fargs=, repeat = False)

plt.draw()
plt.show()