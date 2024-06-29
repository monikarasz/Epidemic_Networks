from ModelCommon import ModelCommon
import numpy as np


class SIS(ModelCommon):
    def __init__(self, G, pos, size, healthy, infected, color_dict, b, g, node_size=20, width=1,
                 immunization=False, strategy=None, max_steps=100, model_name=None, frac_im = 0.1):#added frac_im
        super().__init__(G, pos, size, healthy, infected, color_dict, node_size, width)
        self.model_name = 'SIS' if model_name is None else model_name
        self.b = b
        self.g = g
        self.n_infected = [len(infected)]
        self.immunization = immunization
        self.strategy = strategy
        self.immunized = []
        self.n_immunized = [len(self.immunized)]
        self.n_targets = int(size*frac_im)#changed this
        #self.n_targets = max(size // max_steps, 1)
        self.max_steps = max_steps

    def stop_condition(self):
        return (len(self.n_infected) > 10 and np.average(self.n_infected[-10:]) < 1) or self.run_time > self.max_steps

    def evolve_one_node(self, i):
        node_health = self.G.nodes[i]['health']
        if node_health == 3:
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
            if np.random.random() <= self.g:
                self.G.nodes[i]['health'] = 0
                self.infected.remove(i)
                self.healthy.append(i)

    def immunize(self):
        targets = self.strategy(self.G, self.n_targets)
        for target in targets:
            self.G.nodes[target]['health'] = 3
            if target not in self.immunized:
                self.immunized.append(target)
                #if target in self.infected:
                #    self.infected.remove(target)
                #else:
                #    self.healthy.remove(target)

    def evolve_all(self):
        super().evolve_all()
        #self.immunize()
        self.n_infected.append(len(self.infected))
        #self.n_immunized.append(len(self.immunized))


    def get_infected_history(self):
        return self.n_infected

    def get_immunization_history(self):
        return self.n_immunized
