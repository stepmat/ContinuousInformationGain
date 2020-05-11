import csv 
import sys
import math

import bigfloat

#AgentName
#GameName
#totalNumber
#AverageWin
#AverageScore
#AverageTime
#STDWin
#STDScore
#STDTime

all_data = []
games = []
agents = []

with open('Combined_raw_data.csv', 'r') as csvfile:
    rr = csv.reader(csvfile)
    for row in rr:
        all_data.append(row)
        games.append(row[1])
        agents.append(row[0])

agents = list(set(agents))
games = list(set(games))

agents.sort()
games.sort()

print(len(all_data))
print(agents)
print(games)

num_agents = len(agents)

for i in range(len(all_data)):
    for j in range(len(all_data[i])):
        if j > 1:
            all_data[i][j] = float(all_data[i][j])

new_info_gain = []

#conf_mats = []
info_gains = []
for g in games:
    conf_mat = []
    print("new game")
    print(g)
    for a1 in agents:
        total_for_row = 0
        conf_mat.append([])
        a1_data = None
        for row in all_data:
            if ((row[0] == a1) and (row[1] == g)):
                a1_data = row
        for a2 in agents:
            a2_data = None
            for row2 in all_data:
                if ((row2[0] == a2) and (row2[1] == g)):
                    a2_data = row2
            val = (a1_data[4] - a2_data[4])*(a1_data[4] - a2_data[4])
            val = val / (2*((a1_data[7] + a2_data[7])*(a1_data[7] + a2_data[7])))
            val = 0.0-val
            val = bigfloat.exp(val,bigfloat.precision(100))
            val = val / (math.sqrt((2*math.pi)*((a1_data[7] + a2_data[7])*(a1_data[7] + a2_data[7]))))

            val = float(val)

            conf_mat[-1].append(val)

            total_for_row = total_for_row + val

        for ii in range(len(conf_mat[-1])):
            conf_mat[-1][ii] = conf_mat[-1][ii] / total_for_row
            if conf_mat[-1][ii] <= 0.0:
                conf_mat[-1][ii] = 0.00001

    print(conf_mat[0][1])
    print(conf_mat[1][0])
    print(conf_mat[0])

    total_info = math.log(num_agents,2)
    info2 = 0
    for i in range(num_agents):
        info1 = 0
        for j in range(num_agents):
            info1 = info1 - (conf_mat[i][j] * (math.log(conf_mat[i][j],2)))
        info2 = info2 + ((1.0 / num_agents) * info1)
    total_info = total_info - info2

    if total_info < 0.0:
        total_info = 0.0

    info_gains.append(total_info)

    print(total_info)

for j in range(len(info_gains)):
    print(games[j] + ", " + str(info_gains[j]))


