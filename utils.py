import networkx as nx
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import io
import imageio.v2 as imageio
import os

matplotlib.use('TkAgg')


def get_graph_by_type(graph_type, size, params):
    if graph_type == 'nws':
        return nx.newman_watts_strogatz_graph(size, params['neighbors_connected'], params['prob_connection'])
    if graph_type == 'sf':
        return nx.scale_free_graph(size)


def new_graph(size, initial_infections, graph_type, params):
        G = get_graph_by_type(graph_type, size, params)

        pos = nx.spring_layout(G, seed=225)
        initial = np.zeros(size)#all healthy
        random_infections = np.random.randint(0,high=size,size=initial_infections) #randomly choose infected nodes
        initial[random_infections] = 1 #chosen nodes become infected
        initial_dict = dict(enumerate(initial, 0))
        nx.set_node_attributes(G,initial_dict,"health")
        healthy = [x for x,y in G.nodes(data=True) if y['health']==0]
        infected = [x for x,y in G.nodes(data=True) if y['health']==1]
        return G, healthy, infected, pos


def draw_graph(G, pos, colors, model_name, name):
    steps_dir = 'plots/' + model_name + '/steps'
    if not os.path.exists(steps_dir):
        os.makedirs(steps_dir)

    fig, ax = plt.subplots()
    nx.draw(G, pos, node_size=20, node_color=colors)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    image = imageio.imread(buf)
    imageio.imwrite(steps_dir + f'/{name}.png', image)
    return image


def make_gif(frame_list, model_name, name):
    save_dir = 'plots/' + model_name
    imageio.mimsave(save_dir + f'/{name}.gif', frame_list, duration=1)


def draw_evolution(evolution, t, model_name, name, label):
    save_dir = 'plots/' + model_name
    plt.plot(np.arange(t + 1), evolution)
    plt.xlabel('time step')
    plt.ylabel(label)
    plt.savefig(save_dir + f'/{name}.png')
    plt.close()
