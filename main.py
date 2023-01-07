import networkx as nx
import matplotlib.pyplot as plt

activities = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
durations = [7, 9, 3, 8, 5, 4, 2, 1]
predecessors = ['', 'A', 'A', 'B', 'C', 'C', 'DEF', 'G']

successors = [] #['BC', 'D', 'EF', 'G', 'G', 'G', 'H', '']

ES = [] #Early Start
EF = [] #Early Finish
LS = [] #Late Start
LF = [] #Late Finish
SK = [] #Slack Value

G = nx.DiGraph()

for i in range(len(activities)):
    successors.append('')

print("Edges:")
for i in range(len(activities)):

    if(i == 0):
        ES.append(0)
        EF.append(durations[0])

    else:
        max = 0

        for j in range(len(predecessors[i])):
            G.add_edge(predecessors[i][j], activities[i])
            print(predecessors[i][j], "->", activities[i])
            successors[activities.index(predecessors[i][j])] += activities[i];

            if(EF[activities.index(predecessors[i][j])] > max):
                max = EF[activities.index(predecessors[i][j])]

        ES.append(max)
        EF.append(max + durations[i])

print("Successors:")
for i in successors:
    print(i)     

print("-----------ES-----------")
for i in ES:
    print(i)

print("-----------EF-----------")
for i in EF:
    print(i)


size = len(activities) 

print("Start")
for i in range(len(activities)):
    if(i == 0):
        LF.append(EF[size - 1])
        LS.append(LF[0] - durations[size - 1])

    else:
        min = 1000000000000

        for j in range(len(successors[size - i - 1])):

            if(LS[size - 1 - activities.index(successors[size - i - 1][j])] < min):
                print("IN")
                min = LS[size - 1 - activities.index(successors[size - i - 1][j])]

        LF.append(min)
        LS.append(min - durations[size - i - 1])


LS.reverse()
LF.reverse()

print("-----------LS-----------")
for i in LS:
    print(i)

print("-----------LF-----------")
for i in LF:
    print(i)

for i in range(len(activities)):
    SK.append(LS[i] - ES[i])


print("-----------SK-----------")
for i in SK:
    print(i)        

color_map = []
for node in G:
    print(activities.index(node))
    if(SK[activities.index(node)]) == 0:
        color_map.append('red')
    else:
        color_map.append('green')


pos = nx.spring_layout(G, seed=12)
for k,v in pos.items():
    pos[k]=(-v[1],v[0])

nx.draw_networkx_nodes(G,pos = pos, node_shape = 'o', node_size = 300, 
                        node_color = color_map, edgecolors='k')
nx.draw_networkx_edges(G,pos = pos, 
                        node_shape = 's', width = 1,  node_size = 200)
nx.draw_networkx_labels(G,pos = pos, font_size = 12)

plt.savefig("test")

start_times = []
end_times = []
print('ES: ',ES[1])
for i in range(len(activities)):
    print('i: ',i)

    start_times.append(ES[i])

    end_times.append(EF[i])

# Stwórz pusty wykres
fig, ax = plt.subplots()

# Iteruj przez wszystkie zadania i rysuj na wykresie odpowiednie prostokąty
for i, task in enumerate(reversed(activities)):
    ax.barh(i, end_times[len(activities) - i -1] - start_times[len(activities) - i -1], left=start_times[len(activities) - i -1], height=0.5, label=task)

# Dodaj opisy osi i etykiety zadań
ax.set_yticks(range(len(activities)))
ax.set_yticklabels(reversed(activities))
ax.set_xlabel('Czas')

plt.savefig('wykres.png')
