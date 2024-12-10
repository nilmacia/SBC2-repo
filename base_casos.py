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
                return
            else:
                dist = np.sqrt(np.sum(((case - self.cases) * d_weights)**2, -1))
                closest = self.cases[np.argmin(dist)]
                self.cases = np.concat([self.cases, [case]])
                return closest
        
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