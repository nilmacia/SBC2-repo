import numpy as np

layer_th = [
    [2, 4, 8],        # nombre
    [10, 20, 40, 70], # edat
    [120, 300, 600, 1800],  # temps
]

class Arbre:
    def __init__(self, i=0, maxsize=10000):
        if i < len(layer_th):
            self.children = [Arbre(i+1) for _ in range(len(layer_th) + 1)]
        else:
            self.casos = set()
        self.i = i
        self.maxsize = maxsize

    def __search_leaf(self, cas):
        if self.i < len(layer_th):
            for th, child in zip(layer_th[self.i], self.children):
                if cas.classificadors[self.i] < th:
                    return child.__search_leaf(cas)
            return self.children[-1].__search_leaf(cas)
        else:
            return self

    def fetch(self, cas):
        leaf = self.__search_leaf(cas)
        return leaf.casos

    def feed(self, cas):
        leaf = self.__search_leaf(cas)
        leaf.casos.add(cas)

    def recorre_fulles(self):
        casos = set()
        if self.i < len(layer_th):
            for child in self.children:
                casos |= child.recorre_fulles()
        else: 
            casos |= self.casos
        return casos
    
    def __mantenir(self, v1, v2):
        if self.i < len(layer_th):
            casos_inutils = set()
            for child in self.children:
                casos_inutils |= child.__mantenir(v1, v2)
            return casos_inutils
        else:
            casos_inutils = {cas for cas in self.casos if v1 < cas.valoracio < v2}
            self.casos -= casos_inutils
            return casos_inutils

    def mantenir(self):
        casos = self.recorre_fulles()
        while len(casos) > self.maxsize:
            v1, v2 = np.percentile([cas.valoracio for cas in casos], [49,51])
            casos -= self.__mantenir(v1, v2)