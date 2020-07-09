import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math
import psycopg2
from postgis import Polygon,MultiPolygon,LineString
from postgis.psycopg import register


#Coimbra
#center_lon = -23602.1779130802
#center_lat = 59444.2411470825

#Porto
#center_lon = -41601.3030699869
#center_lat = 165663.59287178 

#Lisboa
center_lon = -87973.4688070632
center_lat = -103263.891293955

#Sintra
#center_lon = -108167.564175462
#center_lat = -95655.0195241774

scale=1/30000
zoom = 10000

plt.style.use('dark_background')
xs_min, xs_max, ys_min, ys_max = center_lon - zoom, center_lon + zoom, center_lat - zoom, center_lat + zoom 

width_in_inches = (xs_max-xs_min)/0.0254*1.1
height_in_inches = (ys_max-ys_min)/0.0254*1.1
fig, ax = plt.subplots(figsize=(width_in_inches*scale, height_in_inches*scale))
ax.axis('off')
ax.set(xlim=(xs_min, xs_max), ylim=(ys_min, ys_max))

conn = psycopg2.connect("dbname=tabd user=postgres password=11223344Ab")
register(conn)
cursor_psql = conn.cursor()

#sql = "select proj_track from tracks where st_intersects('SRID=3763;" + str(porto) + "', proj_track)"
#sql = "select proj_track from tracks"
sql = "select proj_track from tracks where st_intersects((select st_union(proj_boundary) from cont_aad_caop2018 where concelho = 'LISBOA'), proj_track)"
cursor_psql.execute(sql)

results = cursor_psql.fetchall()
#print(results)
cont = 0

for track in results:
    if type(track[0]) is LineString:
        xy = track[0].coords
        xxx = []
        yyy = []
        first = 1
        for (x,y) in xy:
            if first == 1:
                xxx.append(x)
                yyy.append(y)
                previousx=x
                previousy=y
                first = 0
            elif math.sqrt(abs(x-previousx)**2+abs(y-previousy)**2)<50:
                xxx.append(x)
                yyy.append(y)
                previousx=x
                previousy=y
        ax.plot(xxx,yyy,linewidth=0.2,color='white')

plt.savefig('Lisboa.png')
