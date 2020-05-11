import csv 
import sys
import math
import bigfloat
import copy

#input csv label order 
#[AgentName,GameName,totalNumber,AverageWin,AverageScore,AverageTime,STDWin,STDScore,STDTime]

all_data = []
games = []
agents = []

number_games = 10                           #The number of games you want to select

#read in the csv file
with open('Combined_raw_data.csv', 'r') as csvfile:
    input_csv = csv.reader(csvfile)
    for row in input_csv:
        all_data.append(row)
        games.append(row[1])
        agents.append(row[0])

#sort and order the input data
agents = list(set(agents))
games = list(set(games))
agents.sort()
games.sort()
num_agents = len(agents)

#convert all numbers to floats
for i in range(len(all_data)):
    for j in range(len(all_data[i])):
        if j > 1:
            all_data[i][j] = float(all_data[i][j])

chosen_games = []           #chosen games based on information gain
info_gain_history = []      #info gain of all chosen games after each new game is added

while (len(chosen_games) < number_games):
    info_gains = []
    for g in games:         #compute confusion matrix for each game
        conf_mat = []
        print(g)

        for a1 in agents:
            total_for_row = 0.0
            conf_mat.append([])
            a1_data = []

            for row in all_data:
                if ((row[0] == a1) and (row[1] == g)):
                    a1_data.append(row)
                if ((row[0] == a1) and (row[1] in chosen_games)):
                    a1_data.append(row)

            for a2 in agents:
                a2_data = []
                for row2 in all_data:
                    if ((row2[0] == a2) and (row2[1] == g)):
                        a2_data.append(row2)
                    if ((row2[0] == a2) and (row2[1] in chosen_games)):
                        a2_data.append(row2)

                # calculate p(a2|a1) for every pair of agents a1 and a2

                val_n = 0.0       #numerator value
                val_d = 1.0       #denominator value

                for i in range(len(a1_data)):
                    val1 = (a1_data[i][3] - a2_data[i][3])*(a1_data[i][3] - a2_data[i][3])
                    val1 = val1 / (2*((a1_data[i][6] + a2_data[i][6])*(a1_data[i][6] + a2_data[i][6])))
                    val2 = (a1_data[i][4] - a2_data[i][4])*(a1_data[i][4] - a2_data[i][4])
                    val2 = val2 / (2*((a1_data[i][7] + a2_data[i][7])*(a1_data[i][7] + a2_data[i][7])))
                    val_n = val_n + val1+val2

                val_n = 0.0-val_n
                val_n = bigfloat.exp(val_n,bigfloat.precision(100))

                for i in range(len(a1_data)):
                
                    val3 = (math.sqrt((2*math.pi)*((a1_data[i][6] + a2_data[i][6])*(a1_data[i][6] + a2_data[i][6]))))
                    val4 = (math.sqrt((2*math.pi)*((a1_data[i][7] + a2_data[i][7])*(a1_data[i][7] + a2_data[i][7]))))
                    val_d = val_d * (val3*val4)

                val = val_n / val_d
                val = float(val)
                conf_mat[-1].append(val)
                total_for_row = total_for_row + val     # keep a total for row to divide all elements by

            for ii in range(len(conf_mat[-1])):
                conf_mat[-1][ii] = conf_mat[-1][ii] / total_for_row
                if conf_mat[-1][ii] <= 0.0:
                    conf_mat[-1][ii] = 0.00001

        total_info = math.log(num_agents,2)
        info2 = 0.0

        #display confusion matrix with values rounded to 3dp
        conf_mat_print = copy.deepcopy(conf_mat)
        for i in range(len(conf_mat_print)):
            for j in range(len(conf_mat_print[i])):
                conf_mat_print[i][j] = round(conf_mat_print[i][j],3)
        print(conf_mat_print)

        #calculate information gain for each game using its confusion matrix
        for i in range(num_agents):
            info1 = 0.0
            for j in range(num_agents):
                info1 = info1 - (conf_mat[i][j] * (math.log(conf_mat[i][j],2)))
            info2 = info2 + ((1.0 / num_agents) * info1)
        total_info = total_info - info2

        if total_info < 0.0:
            total_info = 0.0

        print(total_info)
        print("")

        info_gains.append(total_info)

    #select game with most (added) information gain to add to set of chosen games
    max_info_gain = 0.0
    max_game = None
    for i in range(len(info_gains)):
        if info_gains[i] > max_info_gain:
            max_info_gain = info_gains[i]
            max_game = i

    for i in range(len(info_gains)):
        print(games[i] + ", " + str(info_gains[i]))

    print("THE CHOSEN GAME")
    print(games[max_game])
    print(len(chosen_games)+1)
    print("")

    info_gain_history.append(max_info_gain)
    chosen_games.append(games[max_game])
    games.pop(max_game)

print("FINAL")
print(chosen_games)
print(info_gain_history)

