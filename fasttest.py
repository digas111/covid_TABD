from random import randrange
import csv
import os

# print(randrange(0, 2))

# for i in range (0,3):
#     print(i)

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

# infectedByDistrictAux = [0]*len(districts)
# j=0
# for i in infectedByDistrictAux:
#     print(j)
#     j+=1



# if os.path.exists("fasttest.csv"):
#     os.remove("fasttest.csv")

# for i in range(0,10):
#     first = True
#     for j in range(20,50):
#         if (first):
#             simulateInfectionf = open("fasttest.csv", "a")
#             simulateInfectionf.write(str(i) + " " + str(j))
#             simulateInfectionf.close()
#             first = False
#         else:
#             simulateInfectionf = open("fasttest.csv", "a")
#             simulateInfectionf.write("," + str(i) + " " + str(j))
#             simulateInfectionf.close()
#     simulateInfectionf = open("fasttest.csv", "a")
#     simulateInfectionf.write("\n")
#     simulateInfectionf.close()



for i in range(0,10):
    if (i+1 < 5):
        print("i:" + str(i))



