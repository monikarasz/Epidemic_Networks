import utils
import strategies
from SIS import SIS
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
matplotlib.use('TkAgg')



size = 1500
max_steps = 50
num_iterations = 10
graph_params = {'m': 3, 'p': 0.1}
G, healthy, infected, pos = utils.new_graph(size=size, initial_infections=0, graph_type='sf', params=graph_params)
im_fracs = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99]
name = 'scale_free_1'

strats = [strategies.random_immunization, strategies.selective_immunization]
strat_names = ['random', 'targeted']
avgs = [[] for _ in range(len(strats))]
vars = [[] for _ in range(len(strats))]

def reset_graph(G):
    for n in G.nodes:
        G.nodes[n]['health'] = 0
    healthy = list(G.nodes)
    infected = []
    return G, healthy, infected



for frac_im in im_fracs:
    print('Running for value: ' + str(frac_im))
    for i in range(len(strats)):
        infected_percent = []
        for _ in range(num_iterations):
            model = SIS(G=G, pos=pos, size=size, healthy=healthy, infected=infected, color_dict=None, b=0.2, g=0.3, immunization=True, strategy=strats[i], model_name='none', max_steps=max_steps, node_size=4, width=0.2, frac_im=frac_im)
            model.infect_random(10)
            model.run_evolution()
            infected_percent.append(model.get_num_infected() / size)
            G, healthy, infected = reset_graph(G)
        avgs[i].append(np.average(infected_percent))
        vars[i].append(np.var(infected_percent))


plt.figure(figsize=(10, 6))

for i in range(len(strats)):
    devs = np.sqrt(vars[i])
    plt.errorbar(im_fracs, avgs[i], yerr=devs, fmt='-o', capsize=5, label=strat_names[i])

plt.title('Comparison of Strategies')
plt.xlabel('fraction immunized')
plt.ylabel('fraction infected')
plt.legend()

if not os.path.exists('final_plots/'):
    os.makedirs('final_plots/')
plt.savefig('final_plots/' + name + '.png')
