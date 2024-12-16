import json
import pandas as pd

with open("dades/domini.json") as f:
    __domini = json.load(f)
noms = {
    'artistes': pd.Series(list(__domini['artistes'])),
    'periodes': pd.Series(list(__domini['periodes'])),
    'obres': pd.read_csv('dades/obres.csv').Title
}

class Cas:
    def __init__(self, nombre, edat, t_dia, dies, artistes, periodes):
        self.nombre = nombre
        self.edat = edat
        self.temps = t_dia * dies
        self.dies = dies
        self.artistes = artistes
        self.periodes = periodes
        self.valoracio = None
        self.obres = None

    @property
    def classificadors(self):
        return self.nombre, self.edat, self.temps
    
    @property
    def noms_artistes(self):
        return list(noms['artistes'][self.artistes])
    
    @property
    def noms_periodes(self):
        return list(noms['periodes'][self.periodes])
    
    @property
    def noms_obres(self):
        return list(noms['obres'][self.obres])