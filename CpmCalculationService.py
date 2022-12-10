import random
import string

import networkx as nx
import matplotlib.pyplot as plt

BIG_INT = 1000000000000


class CpmCalculationService:

    def __init__(self):
        self.successors = []
        self.G = None

    def calculate(self, activities, durations, predecessors):

        self.validate_input(activities, durations, predecessors)

        self.successors = []
        self.G = nx.DiGraph()
        wyniki = []

        for i in range(len(activities)):
            self.successors.append('')

        wyniki, es, ef = self.calculate_and_add_edges(predecessors, activities, durations, wyniki)

        self.generate_graph()

        wyniki, ls = self.calculate_and_add_late(ef, durations, activities, wyniki)

        wyniki = self.calculate_and_add_slack(ls, es, activities, wyniki)

        return wyniki

    def calculate_and_add_edges(self, predecessors, activities, durations, wyniki):
        es = []
        ef = []

        wyniki.append("Edges:")
        for i in range(len(activities)):

            if i == 0:
                es.append(0)
                ef.append(durations[0])

            else:
                local_max = 0

                for j in range(len(predecessors[i])):
                    self.G.add_edge(predecessors[i][j], activities[i])
                    wyniki.append(predecessors[i][j] + "->" + activities[i])
                    self.successors[activities.index(predecessors[i][j])] += activities[i]

                    if ef[activities.index(predecessors[i][j])] > local_max:
                        local_max = ef[activities.index(predecessors[i][j])]

                es.append(local_max)
                ef.append(local_max + durations[i])

        wyniki.append("self.successors:")
        for i in self.successors:
            wyniki.append(i)

        wyniki.append("-----------ES-----------")
        for i in es:
            wyniki.append(i)

        wyniki.append("-----------EF-----------")
        for i in ef:
            wyniki.append(i)

        return wyniki, es, ef

    def calculate_and_add_late(self, ef, durations, activities, wyniki):
        lf = []
        ls = []

        size = len(activities)

        wyniki.append("Start")
        for i in range(len(activities)):
            if i == 0:
                lf.append(ef[size - 1])
                ls.append(lf[0] - durations[size - 1])

            else:
                min_duration = BIG_INT

                for j in range(len(self.successors[size - i - 1])):

                    if ls[size - 1 - activities.index(self.successors[size - i - 1][j])] < min_duration:
                        wyniki.append("IN")
                        min_duration = ls[size - 1 - activities.index(self.successors[size - i - 1][j])]

                lf.append(min_duration)
                ls.append(min_duration - durations[size - i - 1])

        ls.reverse()
        lf.reverse()

        wyniki.append("-----------LS-----------")
        for i in ls:
            wyniki.append(i)

        wyniki.append("-----------LF-----------")
        for i in lf:
            wyniki.append(i)

        return wyniki, ls

    def calculate_and_add_slack(self, ls, es, activities, wyniki):
        sk = []

        for i in range(len(activities)):
            sk.append(ls[i] - es[i])

        wyniki.append("-----------SK-----------")
        for i in sk:
            wyniki.append(i)

        return wyniki

    def validate_input(self, activities, durations, predecessors):
        if len(activities) == len(durations) and len(durations) == len(predecessors):
            pass
        else:
            raise ValueError("Number of elements in arrays differ")

    def generate_file_name(self, prefix):
        return prefix + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))

    def generate_graph(self):
        pos = nx.spring_layout(self.G, seed=12)
        for k, v in pos.items():
            pos[k] = (-v[1], v[0])

        nx.draw_networkx_nodes(self.G, pos=pos, node_shape='o', node_size=300,
                               node_color='none', edgecolors='k')
        nx.draw_networkx_edges(self.G, pos=pos,
                               node_shape='s', width=1, node_size=200)
        nx.draw_networkx_labels(self.G, pos=pos, font_size=11)

        plt.savefig(self.generate_file_name("resources/test_"))
