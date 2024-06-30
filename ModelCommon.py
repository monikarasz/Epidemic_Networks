import utils


class ModelCommon:
    def __init__(self, G, pos, size, healthy, infected, color_dict, node_size=20, width=1.0):
        self.model_name = 'common'
        self.G = G
        self.pos = pos
        self.size = size
        self.color_dict = color_dict
        self.healthy = healthy
        self.infected = infected
        self.run_time = 0
        self.node_size = node_size
        self.width = width
        self.visualize = False

    def stop_condition(self):
        pass

    def evolve_one_node(self, i):
        pass

    def evolve_all(self):
        for i in range(self.size):  # expose all healthy nodes to their infected neighbors
            self.evolve_one_node(i)

    def run_evolution(self):
        self.run_time = 0
        frames = []
        while not self.stop_condition():
            self.evolve_all()
            if self.visualize:
                health_now = dict(self.G.nodes('health'))
                colors = [self.color_dict[health_now[x]] for x in health_now]
                image = utils.draw_graph(self.G, self.pos, colors, self.model_name, f'step_{self.run_time}', self.node_size, self.width)
                frames.append(image)
            self.run_time += 1
        if self.visualize:
            utils.make_gif(frames, self.model_name, 'graph_evolution')

    def get_run_time(self):
        return self.run_time

    def get_num_infected(self):
        return len(self.infected)
