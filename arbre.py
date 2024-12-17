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
        casos = []
        if self.i < len(layer_th):
            for child in self.children:
                casos.extend(child.recorre_fulles()) 
        else: 
            casos.extend(self.casos)
        return casos