from ModelCommon import ModelCommon
import numpy as np


class SIS(ModelCommon):
    def __init__(self, G, pos, size, healthy, infected, color_dict, b, g):
        super().__init__(G, pos, size, healthy, infected, color_dict)
        self.model_name = 'SIS'
        self.b = b
        self.g = g
        self.n_infected = [len(infected)]

    def stop_condition(self):
        return (len(self.infected) == 0 or len(self.n_infected)>100)

    def evolve_one_node(self, i):
        node_health = self.G.nodes[i]['health']
        if node_health == 0:
            n_inf = len([self.G.nodes[n]['health'] for n in self.G.neighbors(i) if self.G.nodes[n]['health'] == 1])  # number of infected neighbors
            prob_not_infected = (1 - self.b) ** n_inf  # probability of remaining healthy despite having n_inf infected neighbors
            # we draw a random number from a uniform dist, if it's larger than prob_not_infected, the node gets infected
            if np.random.random() >= prob_not_infected:
                self.G.nodes[i]['health'] = 1
                self.infected.append(i)
                self.healthy.remove(i)
        if node_health == 1:
            if np.random.random() <= self.g:
                self.G.nodes[i]['health'] = 0
                self.infected.remove(i)
                self.healthy.append(i)


    def evolve_all(self):
        super().evolve_all()

        self.n_infected.append(len(self.infected))


    def get_infected_history(self):
        return self.n_infected