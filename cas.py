import json
import pandas as pd
import numpy as np

with open("dades/domini.json") as f:
    __domini = json.load(f)
noms = {
    'artistes': pd.Series(list(__domini['artistes'])),
    'periodes': pd.Series(list(__domini['periodes'])),
    'obres': pd.read_csv('dades/obres.csv').Titol
}

class Cas:
    def __init__(self, nombre, edat, t_dia, dies, artistes, periodes):
        if len(artistes) > 0 and isinstance(artistes[0], str):
            artistes = noms['artistes'].isin(artistes).to_numpy()
        if len(periodes) > 0 and isinstance(periodes[0], str):
            periodes = noms['periodes'].isin(periodes).to_numpy()

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

    @staticmethod
    def guardar(casos, path):
        casos = [
            [cas.nombre, cas.edat, cas.temps, cas.dies,
             *cas.artistes, *cas.periodes, *cas.obres, cas.valoracio]
        for cas in casos]
        casos = np.array(casos)
        np.save('dades/casos', casos)