import numpy as np
from itertools import permutations

d_weights = np.array([1,1,1,1,1,1,1,1,1])

class Node:
    def __init__(self, i=None, thresholds=None, children=None):
        if i is not None:
            self.i = i
            self.thresholds = thresholds
            self.children = children
        else:
            self.cases = None

    def feed(self, case):
        if 'i' in dir(self):
            for th, child in zip(self.thresholds, self.children):
                if case[self.i] < th:
                    return child.feed(case)
            return self.children[-1].feed(case)
        else:
            if self.cases is None:
                self.cases = np.stack([case])
                return self.cases  # Retornem els casos emmagatzemats (només un en aquest punt)
            else:
                return self.cases  # Retornem tots els casos emmagatzemats a la fulla

        
layer_thresholds = [
    [1, 5], 
    [14, 65],   
    [2, 4], 
    [1, 2],
    [1 ,2 ,3]
    #[1],
    #[1],
    #[1],
    #[1],
    #[1]
    ]

#Hi han tres funcions que permeten trobar l'ordre òptim de larbre per a que estigui més balancejat i sigui més eficient

def evaluate_balance(cases, i, thresholds):
    """
    Calcula una mesura de desequilibri per una característica amb un ordre específic de thresholds.
    """
    counts = []
    for th in thresholds:
        counts.append(np.sum(cases[:, i] < th))
        cases = cases[cases[:, i] >= th]
    counts.append(len(cases)) 
    return np.var(counts) 


def find_optim_threshold_order(cases, i, thresholds):
    """
    Troba l'ordre de thresholds que minimitza el desequilibri per una característica `i`.
    """
    best_order = None
    min_variance = float('inf')

    for perm in permutations(thresholds):  # Prova totes les permutacions
        variance = evaluate_balance(cases, i, perm)
        if variance < min_variance:
            min_variance = variance
            best_order = perm

    return list(best_order), min_variance

def optimize_thresholds(cases, layer_thresholds):
    """
    Retorna l'ordre òptim dels thresholds per cada característica.
    """
    optimized_thresholds = []
    for i, thresholds in enumerate(layer_thresholds):
        if len(thresholds) > 1:
            best_order, _ = find_optim_threshold_order(cases, i, thresholds)
            optimized_thresholds.append(best_order)
        else:
            optimized_thresholds.append(thresholds)  # Si només hi ha un llindar, no hi ha res a optimitzar
    return optimized_thresholds


optimized_thresholds = optimize_thresholds(layer_thresholds)

node_stack = [Node() for _ in range(sum(len(th) + 1 for th in optimized_thresholds))]

for i, thresholds in reversed(list(enumerate(optimized_thresholds))):
    num_nodes_at_level = len(thresholds) + 1
    for _ in range(num_nodes_at_level):
        node = Node(i, thresholds, node_stack[:len(thresholds) + 1])
        node_stack.append(node)
        del node_stack[:len(thresholds) + 1]

root = node_stack[0]

from carregar_casos import load
casos = load()
print(root.feed(casos[0]))
print(root.feed(casos[2]))
print(root.feed(casos[1]))
print(root.feed(casos[0]))

from cas import *
Cas()
