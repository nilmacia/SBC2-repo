import json
import numpy as np

path_domini = "dades/domini.json"

class Cas:
    def __init__(self, nombre, edat, t_dia, dies, tipus, artistes, periodes):
        self.nombre = nombre
        self.edat = edat
        self.temps = t_dia * dies
        self.dies = dies
        self.tipus = tipus
        self.artistes = artistes
        self.periodes = periodes
        self.valoracio = None
        self.obres = None

    def set_obres(self, obres):
        self.obres = obres
    
    def set_valoracio(self, valoracio):
        self.valoracio = valoracio

    def array_feats(self) -> np.ndarray:
        atributs = np.array([self.nombre, self.edat, self.temps, self.dies, self.tipus, self.valoracio])

        with open(path_domini) as f:
            domini = json.load(f)
        
        artistes = np.isin(list(domini["artistes"]), self.artistes).astype(int)
        periodes = np.isin(list(domini["periodes"]), self.periodes).astype(int)
        
        return np.concat([atributs, artistes, periodes])

    def array_obres(self) -> np.ndarray:
        """
        Retorna el vector binari per les obres recomanades
        """

        with open(path_domini) as f:
            domini = json.load(f)
        
        return np.isin(domini["obres"], self.obres).astype(int)