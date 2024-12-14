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

node_stack = [Node() for _ in range(sum(len(th) + 1 for th in layer_thresholds))]

for i, thresholds in reversed(list(enumerate(layer_thresholds))):
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
