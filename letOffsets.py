
import numpy as np
import matplotlib.pyplot as plt
import psycopg2
import math
from matplotlib.animation import FuncAnimation
import datetime
import csv
from postgis import Polygon,MultiPolygon
from postgis.psycopg import register


with open('simulateInfection.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    frame=0
    i=0
    
    for row in reader:  
        print(row)
        if(frame == i):
            for item in row:
                x,y,color = item.split()
                print("x: " + x + " y: " + y + " color: " + color)
        frame+=1

#line.append(buffer.split(","))
