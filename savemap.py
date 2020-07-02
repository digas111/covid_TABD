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
from multiprocessing import Process

cPorto = ['Porto','VILA NOVA DE GAIA', 'MATOSINHOS','MAIA']
cLisboa = ['LISBOA','OEIRAS','CASCAIS','SINTRA','AMADORA','ODIVELAS','LOURES','ALMADA','SEIXAL','MOITA']


conn2 = psycopg2.connect("dbname=postgres user=postgres")
register(conn2)
cursor_psql = conn2.cursor()

sql = "select distrito,st_union(proj_boundary) from cont_aad_caop2018 group by distrito"

cursor_psql.execute(sql)
results = cursor_psql.fetchall()

folder = os.getcwd()+"/maps/"

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


with open(folder + 'portugal.csv', 'w', newline='') as portugal:
    portugalw = csv.writer(portugal)
    for row in results:
        geom = row[1]
        if type(geom) is MultiPolygon:
            for pol in geom:
                xys = pol[0].coords
                points = []
                for (x,y) in xys:
                    points.append(str(x) + " " + str(y))
                portugalw.writerow(points)
        if type(geom) is Polygon:
            xys = geom[0].coords
            points = []
            for (x,y) in xys:
                    points.append(str(x) + " " + str(y))
            portugalw.writerow(points)

### PORTO

sql = "select freguesia, st_union(proj_boundary), concelho from cont_aad_caop2018 where concelho = 'PORTO' or concelho = 'VILA NOVA DE GAIA' or concelho = 'MATOSINHOS' or concelho = 'MAIA' group by concelho,freguesia"

cursor_psql.execute(sql)
results = cursor_psql.fetchall()

with open(folder + 'porto.csv', 'w', newline='') as porto:
    portow = csv.writer(porto)
    for row in results:
        geom = row[1]
        if type(geom) is MultiPolygon:
            for pol in geom:
                xys = pol[0].coords
                points = []
                for (x,y) in xys:
                    points.append(str(x) + " " + str(y))
                portow.writerow(points)
        if type(geom) is Polygon:
            xys = geom[0].coords
            points = []
            for (x,y) in xys:
                    points.append(str(x) + " " + str(y))
            portow.writerow(points)


### LISBOA

sql = "select freguesia, st_union(proj_boundary), concelho from cont_aad_caop2018 where concelho = 'PORTO' or concelho = 'VILA NOVA DE GAIA' or concelho = 'MATOSINHOS' or concelho = 'MAIA' group by concelho,freguesia"

cursor_psql.execute(sql)
results = cursor_psql.fetchall()

with open(folder + 'lisboa.csv', 'w', newline='') as lisboa:
    lisboaw = csv.writer(lisboa)
    for row in results:
        geom = row[1]
        if type(geom) is MultiPolygon:
            for pol in geom:
                xys = pol[0].coords
                points = []
                for (x,y) in xys:
                    points.append(str(x) + " " + str(y))
                lisboaw.writerow(points)
        if type(geom) is Polygon:
            xys = geom[0].coords
            points = []
            for (x,y) in xys:
                    points.append(str(x) + " " + str(y))
            lisboaw.writerow(points)


conn2.close()