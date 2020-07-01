# import numpy as np
# import matplotlib.pyplot as plt
# import psycopg2
# import math
# from matplotlib.animation import FuncAnimation
# import datetime
# import csv
# from postgis import Polygon,MultiPolygon
# from postgis.psycopg import register
# import random

# infectedColor = "#cd0000"

# ##########

# # nInfected = []
# # infectedByDistrict = []

# #####

# districts = {
#     "AVEIRO" : "0",
#     "BEJA" : "1",
#     "BRAGA" : "2",
#     "BRAGANÇA" : "3",
#     "CASTELO BRANCO" : "4",
#     "COIMBRA" : "5",
#     "ÉVORA" : "6",
#     "FARO" : "7",
#     "GUARDA" : "8",
#     "LEIRIA" : "9",
#     "LISBOA" : "10",
#     "PORTALEGRE" : "11",
#     "PORTO" : "12",
#     "SANTARÉM" : "13",
#     "SETÚBAL" : "14",
#     "VIANA DO CASTELO" : "15",
#     "VILA REAL" : "16",
#     "VISEU" : "17"
# }

# conn = psycopg2.connect("dbname=postgres user=postgres")
# register(conn)
# cursor_psql = conn.cursor()

# with open('simulateInfection.csv','r') as csvFile:
#     reader = csv.reader(csvFile)
#     for line in reader:
#         nInfected = 0
#         infectedByDistrict = [0]*len(districts)
#         for row in line:
#             x,y,color = row.split()
#             #print("x:" + x + "y:" + y + "color:" + color)
#             if (color == infectedColor):
#                 nInfected+=1
#                 sql = "select distrito from cont_aad_caop2018 where st_contains(proj_boundary, st_setsrid(st_point(" + str(x) + ", " + str(y) +"), 3763))"
#                 cursor_psql.execute(sql)
#                 results = cursor_psql.fetchall()
#                 if (results != []):
#                     #print("results:" + str(results))
#                     #print(int(districts.get(results[0][0])))
#                     infectedByDistrict[int(districts.get(results[0][0]))] +=1
#         print("%d" %(nInfected),end='')
#         for distr in infectedByDistrict:
#             print(",%d" %(distr),end='')
#         print("")

# conn.close()


