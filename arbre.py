import numpy as np
from itertools import permutations

layer_th = [
    [2, 4, 8],        # nombre
    [10, 20, 40, 70], # edat
    [120, 300, 600, 1800],  # temps
]

class Arbre:
    def __init__(self, i=0):
        if i < len(layer_th):
            self.children = [Arbre(i+1) for _ in range(len(layer_th) + 1)]
        else:
            self.casos = set()
        self.i = i

    def feed(self, cas):
        if self.i < len(layer_th):
            for th, child in zip(layer_th[self.i], self.children):
                if cas.classificadors[self.i] < th:
                    return child.feed(cas)
            return self.children[-1].feed(cas)
        else:
            casos = self.casos.copy()
            self.casos.add(cas)
            # IMPLEMENTAR SELECCIÓ DE CASOS
            return casos