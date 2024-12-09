import numpy as np

d_weights = np.array([1,1,1,1,1,1,1,1,1])

class Node:
    def feed(self, case):
        if 'thresholds' in dir(self):
            if case[self.i] >= self.thresholds[-1]:
                return self.children[-1].feed(case)
            else:
                for th, child in zip(self.thresholds, self.children):
                    if case[self.i] > th:
                        return child.feed(case)
        else:
            dist = np.sqrt(np.sum(((case - self.cases) * d_weights)**2))
            self.cases = np.concat(self.cases, [case])
            return dist