import utils


class ModelCommon:
    def __init__(self, G, pos, size, healthy, infected, color_dict):
        self.model_name = 'common'
        self.G = G
        self.pos = pos
        self.size = size
        self.color_dict = color_dict
        self.healthy = healthy
        self.infected = infected
        self.run_time = 0

    def stop_condition(self):
        pass

    def evolve_one_node(self, i):
        pass

    def evolve_all(self):
        for i in range(self.size):  # expose all healthy nodes to their infected neighbors
            self.evolve_one_node(i)

    def run_evolution(self):
        time = 0
        frames = []
        while not self.stop_condition():
            self.evolve_all()
            health_now = dict(self.G.nodes('health'))
            colors = [self.color_dict[health_now[x]] for x in health_now]
            image = utils.draw_graph(self.G, self.pos, colors, self.model_name, f'step_{time}')
            frames.append(image)
            time += 1
        self.run_time = time
        utils.make_gif(frames, self.model_name, 'graph_evolution')

    def get_run_time(self):
        return self.run_time
