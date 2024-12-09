import numpy as np

d_weights = np.array([1,1,1,1,1,1,1,1,1])

class Node:
    def __init__(self, thresholds=None, children=None):
        if thresholds is not None:
            self.thresholds = thresholds
            self.children = children
        else:
            self.cases = None

    def feed(self, case):
        if 'thresholds' in dir(self):
            if case[self.i] >= self.thresholds[-1]:
                return self.children[-1].feed(case)
            else:
                for th, child in zip(self.thresholds, self.children):
                    if case[self.i] < th:
                        return child.feed(case)
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

nodes = [Node() for _ in range(2**len(d_weights))]

for i in reversed(range(len(d_weights))):
    for _ in range(int(2**(i-1))):
        node = Node(layer_thresholds[i], nodes[:2])
        nodes.append(node)
        del nodes[:2]

root = nodes[0]