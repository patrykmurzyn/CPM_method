import networkx as nx
import matplotlib.pyplot as plt

BIG_INT = 1000000000000


class CpmCalculationService:

    def __init__(self):
        self.successors = []  # ['BC', 'D', 'EF', 'G', 'G', 'G', 'H', '']

    def calculate(self, activities, durations, predecessors):

        self.validate_input(activities, durations, predecessors)

        self.successors = []
        wyniki = []
        ES = []  # Early Start
        EF = []  # Early Finish
        LS = []  # Late Start
        LF = []  # Late Finish
        SK = []  # Slack Value

        G = nx.DiGraph()

        for i in range(len(activities)):
            self.successors.append('')

        wyniki.append("Edges:")
        for i in range(len(activities)):

            if i == 0:
                ES.append(0)
                EF.append(durations[0])

            else:
                max = 0

                for j in range(len(predecessors[i])):
                    G.add_edge(predecessors[i][j], activities[i])
                    wyniki.append(predecessors[i][j] + "->" + activities[i])
                    self.successors[activities.index(predecessors[i][j])] += activities[i];

                    if EF[activities.index(predecessors[i][j])] > max:
                        max = EF[activities.index(predecessors[i][j])]

                ES.append(max)
                EF.append(max + durations[i])

        wyniki.append("self.successors:")
        for i in self.successors:
            wyniki.append(i)

        wyniki.append("-----------ES-----------")
        for i in ES:
            wyniki.append(i)

        wyniki.append("-----------EF-----------")
        for i in EF:
            wyniki.append(i)

        size = len(activities)

        wyniki.append("Start")
        for i in range(len(activities)):
            if i == 0:
                LF.append(EF[size - 1])
                LS.append(LF[0] - durations[size - 1])

            else:
                min_duration = BIG_INT

                for j in range(len(self.successors[size - i - 1])):

                    if LS[size - 1 - activities.index(self.successors[size - i - 1][j])] < min_duration:
                        wyniki.append("IN")
                        min_duration = LS[size - 1 - activities.index(self.successors[size - i - 1][j])]

                LF.append(min_duration)
                LS.append(min_duration - durations[size - i - 1])

        LS.reverse()
        LF.reverse()

        wyniki.append("-----------LS-----------")
        for i in LS:
            wyniki.append(i)

        wyniki.append("-----------LF-----------")
        for i in LF:
            wyniki.append(i)

        for i in range(len(activities)):
            SK.append(LS[i] - ES[i])

        wyniki.append("-----------SK-----------")
        for i in SK:
            wyniki.append(i)

        pos = nx.spring_layout(G, seed=12)
        for k, v in pos.items():
            pos[k] = (-v[1], v[0])

        nx.draw_networkx_nodes(G, pos=pos, node_shape='o', node_size=300,
                               node_color='none', edgecolors='k')
        nx.draw_networkx_edges(G, pos=pos,
                               node_shape='s', width=1, node_size=200)
        nx.draw_networkx_labels(G, pos=pos, font_size=11)

        plt.savefig("test")
        return wyniki

    def validate_input(self, activities, durations, predecessors):
        if len(activities) == len(durations) and len(durations) == len(predecessors):
            pass
        else:
            raise ValueError("Number of elements in arrays differ")
