import numpy as np
import matplotlib.pyplot as plt
import psycopg2
import math
from matplotlib.animation import FuncAnimation
import datetime
from postgis import Polygon,MultiPolygon
from postgis.psycopg import register

conn = psycopg2.connect("dbname=postgres user=postgres")
register(conn)
cursor_psql = conn.cursor()

frame = 1570665600

# sql = "select taxi, st_pointn(proj_track, " + str(frame) + " - ts) from tracks, cont_aad_caop2018 limit 10 "

# sql = "select taxi, st_pointn(proj_track, " + str(frame) + " - ts) from tracks, cont_aad_caop2018 where st_contains(proj_boundary,st_pointn(proj_track, " + str(frame) + " - ts)) limit 10 "

sql = "select taxi, st_pointn(proj_track, " + str(frame) + " - ts) from tracks, cont_aad_caop2018 where distrito in ('PORTO') and st_contains(proj_boundary,st_pointn(proj_track, " + str(frame) + " - ts)) limit 10 "
cursor_psql.execute(sql)
results = cursor_psql.fetchall()

print(len(results))
print(results)


conn.close()



