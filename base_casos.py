import numpy as np

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

        
layer_thresholds = [4, 30, 4, 2, 1, 1, 1, 1, 1]

node_stack = [Node() for _ in range(2**len(d_weights))]

for i in reversed(range(len(d_weights))):
    for _ in range(int(2**i)):
        node = Node(i, [layer_thresholds[i]], node_stack[:2])
        node_stack.append(node)
        del node_stack[:2]

root = node_stack[0]

from carregar_casos import load
casos = load()
print(root.feed(casos[0]))
print(root.feed(casos[2]))
print(root.feed(casos[1]))
print(root.feed(casos[0]))

from cas import *
Cas()


def avaluar_arbre(casos):
    """
    L'he fet amb la variància ponderada quan es podria fer amb el index de gini o qualsevol altre mètode d'avaluació
    Triant el atribut que divideix millor es podria actualitzar l'arbre per aquest atribut
    """
    num_attributes = casos.shape[1]
    best_attribute = None
    best_score = float('inf') 

    for i in range(num_attributes):
        threshold = np.unique(casos[:, i])
        for t in threshold:
            left_cases = casos[casos[:, i] < t]
            right_cases = casos[casos[:, i] >= t]

            if len(left_cases) == 0 or len(right_cases) == 0:
                continue
            score = (len(left_cases) * np.var(left_cases, axis=0).sum() +
                     len(right_cases) * np.var(right_cases, axis=0).sum())

            if score < best_score:
                best_score = score
                best_attribute = (i, threshold)

    return best_attribute