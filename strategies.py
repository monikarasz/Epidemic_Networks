import random


def random_immunization(G, n_targets):
    return random.sample(list(G.nodes), n_targets)

def selective_immunization(G, n_targets):
    g0 = random.sample(list(G.nodes), n_targets)
    g1 = []
    for n in g0:
        neighbors = list(G.neighbors(n))
        if len(neighbors) == 0:
            continue
        target = random.sample(neighbors, 1)
        if target not in g1:
            g1.append(target[0])
    return g1
