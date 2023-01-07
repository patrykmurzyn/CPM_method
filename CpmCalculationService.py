import random
import string

import networkx as nx
import matplotlib.pyplot as plt

BIG_INT = 1000000000000


class CpmCalculationService:


    def calculate(self, activities, durations, predecessors):

        successors = []
        G = None
        wyniki = []
        ES = [] #Early Start
        EF = [] #Early Finish
        LS = [] #Late Start
        LF = [] #Late Finish
        SK = [] #Slack Value

        G = nx.DiGraph()

        for i in range(len(activities)):
            successors.append('')

        wyniki.append("Edges:")
        for i in range(len(activities)):

            if(i == 0):
                ES.append(0)
                EF.append(durations[0])

            else:
                max = 0

                for j in range(len(predecessors[i])):
                    G.add_edge(predecessors[i][j], activities[i])
                    wyniki.append(predecessors[i][j] +  "->" + activities[i])
                    successors[activities.index(predecessors[i][j])] += activities[i];

                    if(EF[activities.index(predecessors[i][j])] > max):
                        max = EF[activities.index(predecessors[i][j])]

                ES.append(max)
                EF.append(max + durations[i])

        wyniki.append("Successors:")
        for i in successors:
            wyniki.append(i[0] + 1, ': ', i[1])

        wyniki.append("-----------ES-----------")
        for i in enumerate(ES):
            wyniki.append(i[0] + 1, ': ', i[1])

        wyniki.append("-----------EF-----------")
        for i in enumerate(EF):
            wyniki.append(i)


        size = len(activities) 

        wyniki.append("Start")
        for i in range(len(activities)):
            if(i == 0):
                LF.append(EF[size - 1])
                LS.append(LF[0] - durations[size - 1])

            else:
                min = 1000000000000

                for j in range(len(successors[size - i - 1])):

                    if(LS[size - 1 - activities.index(successors[size - i - 1][j])] < min):
                        wyniki.append("IN")
                        min = LS[size - 1 - activities.index(successors[size - i - 1][j])]

                LF.append(min)
                LS.append(min - durations[size - i - 1])


        LS.reverse()
        LF.reverse()

        wyniki.append("-----------LS-----------")
        for i in enumerate(LS):
            wyniki.append(i[0] + 1, ': ', i[1])

        wyniki.append("-----------LF-----------")
        for i in enumerate(LF):
            wyniki.append(i[0] + 1, ': ', i[1])

        for i in range(len(activities)):
            SK.append(LS[i] - ES[i])


        wyniki.append("-----------SK-----------")
        for i in SK:
            wyniki.append(i)        

        color_map = []
        for node in G:
            wyniki.append(activities.index(node))
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

        plt.clf()

        start_times = []
        end_times = []
        wyniki.append('ES: '+str(ES[1]))
        for i in range(len(activities)):
            wyniki.append('i: '+str(i))

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

        plt.clf()
        
        return wyniki