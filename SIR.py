from ModelCommon import ModelCommon
import numpy as np


class SIR(ModelCommon):
    def __init__(self, G, pos, size, healthy, infected, color_dict, b, u):
        super().__init__(G, pos, size, healthy, infected, color_dict)
        self.model_name = 'SIR'
        self.b = b
        self.u = u
        self.n_infected = [len(infected)]
        self.n_recovered = [0]
        self.recovered = []

    def stop_condition(self):
        return len(self.infected) == 0

    def evolve_one_node(self, i):
        node_health = self.G.nodes[i]['health']
        if node_health == 2:
            return
        if node_health == 0:
            n_inf = len([self.G.nodes[n]['health'] for n in self.G.neighbors(i) if self.G.nodes[n]['health'] == 1])  # number of infected neighbors
            prob_not_infected = (1 - self.b) ** n_inf  # probability of remaining healthy despite having n_inf infected neighbors
            # we draw a random number from a uniform dist, if it's larger than prob_not_infected, the node gets infected
            if np.random.random() >= prob_not_infected:
                self.G.nodes[i]['health'] = 1
                self.infected.append(i)
                self.healthy.remove(i)
        if node_health == 1:
            if np.random.random() <= self.u:
                self.G.nodes[i]['health'] = 2
                self.infected.remove(i)
                self.recovered.append(i)


    def evolve_all(self):
        super().evolve_all()

        self.n_infected.append(len(self.infected))
        self.n_recovered.append(len(self.recovered))

    def get_infected_history(self):
        return self.n_infected

    def get_recovered_history(self):
        return self.n_recovered

