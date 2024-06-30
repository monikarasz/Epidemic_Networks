import utils
import strategies
from SIS import SIS
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
matplotlib.use('TkAgg')

t = 'nws'

size = 1500
max_steps_list = [50,200]
num_iterations = 20

im_fracs = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99]
if t=='sf':
    name = 'scale-free'
    ms = [2,3, 5, 8]
    ps = [0.05, 0.1, 0.3, 0.5]
elif t=='nws':
    name='nws'
    ms = [2,3, 5, 8]
    ps = [0.05, 0.1, 0.3, 0.5]

strats = [strategies.random_immunization, strategies.selective_immunization]
strat_names = ['random', 'targeted']


def reset_graph(G):
    for n in G.nodes:
        G.nodes[n]['health'] = 0
    healthy = list(G.nodes)
    infected = []
    return G, healthy, infected


def run_sim(im_fracs, max_steps,m,p):
    avgs = [[] for _ in range(len(strats))]
    stds = [[] for _ in range(len(strats))]
    if t=='sf':
        graph_params = {'m': m, 'p': p}
        G, healthy, infected, pos = utils.new_graph(size=size, initial_infections=0, graph_type='sf', params=graph_params)
    elif t=='nws':
        graph_params = {'neighbors_connected': m, 'prob_connection': p}
        G, healthy, infected, pos = utils.new_graph(size=size, initial_infections=0, graph_type='nws', params=graph_params)       
    for frac_im in im_fracs:
        #print('Running for value: ' + str(frac_im))
        for i in range(len(strats)):
            infected_percent = []
            for _ in range(num_iterations):
                model = SIS(G=G, pos=pos, size=size, healthy=healthy, infected=infected, color_dict=None, b=0.2, g=0.3, immunization=True, strategy=strats[i], model_name='none', max_steps=max_steps, node_size=4, width=0.2, frac_im=frac_im)
                model.infect_random(10)
                model.run_evolution()
                infected_percent.append(model.get_num_infected() / size)
                G, healthy, infected = reset_graph(G)
            avgs[i].append(np.average(infected_percent))
            stds[i].append(np.std(infected_percent,ddof=0))
    return avgs, stds

def figures(max_steps, m, p, avgs, stds):
    plt.figure(figsize=(10, 6))

    for i in range(len(strats)):
        #devs = np.sqrt(vars[i])
        plt.errorbar(im_fracs, avgs[i], yerr=stds[i], fmt='-o', capsize=5, label=strat_names[i])
    plt.title('Comparison of Strategies, '+ name + ' graph, m = ' +str(m) + ', p = ' + str(p))
    plt.xlabel('fraction immunized')
    plt.ylabel('fraction infected after ' +str(max_steps) + ' steps')
    plt.xlim(0,1)
    plt.ylim()
    plt.legend()

    if not os.path.exists('final_plots/'+name+'/'):
        os.makedirs('final_plots/'+name+'/')
    plt.savefig('final_plots/'+name+'/' + name + '_s' + str(max_steps) + 'm' +str(m) + 'p' + str(p)+'.png')
    plt.close()


for steps in max_steps_list:
    for m in ms:
        for p in ps:
            
            a, s = run_sim(im_fracs=im_fracs, max_steps=steps,m=m,p=p)
            figures(steps,m,p,a,s)
            print(m,p,steps)

