from ModelCommon import ModelCommon
import numpy as np


class SI(ModelCommon):
    def __init__(self, G, pos, size, healthy, infected, color_dict, b, node_size=20, width=1):
        super().__init__(G, pos, size, healthy, infected, color_dict, node_size, width)
        self.model_name = 'SI'
        self.b = b
        self.n_infected = [len(infected)]

    def stop_condition(self):
        return len(self.infected) >= self.size

    def evolve_one_node(self, i):
        if self.G.nodes[i]['health'] == 1:
            return
        n_inf = len([self.G.nodes[n]['health'] for n in self.G.neighbors(i) if self.G.nodes[n]['health'] == 1])  # number of infected neighbors
        prob_not_infected = (1 - self.b) ** n_inf  # probability of remaining healthy despite having n_inf infected neighbors

        # we draw a random number from a uniform dist, if it's larger than prob_not_infected, the node gets infected
        if np.random.random() >= prob_not_infected:
            self.G.nodes[i]['health'] = 1
            self.infected.append(i)
            self.healthy.remove(i)

    def evolve_all(self):
        super().evolve_all()

        self.n_infected.append(len(self.infected))

    def get_infected_history(self):
        return self.n_infected

