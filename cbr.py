import numpy as np
from generador import valorar
import json
import random
import pandas as pd

with open("dades/domini.json") as f:
    domini = json.load(f)
obres = pd.read_csv('dades/obres.csv')

class CBR:
    def __init__(self, arbre, artist_weight=1., period_weight=1., age_weight=1., time_weight=1.):
        """
        Inicialitza el sistema amb l'arrel i els pesos per artistes, periodes, edat i hores.
        """
        self.arbre = arbre
        self.artist_weight = artist_weight
        self.period_weight = period_weight
        self.age_weight = age_weight
        self.time_weight = time_weight

    def calculate_distance(self, case, leaf_case):
        """
        Calcula la distància entre dos casos, considerant artistes, periodes, edat i hores.
        """
        # Distància conjunta per artistes i periodes (Jaccard combinada)
        artists1, artists2 = set(leaf_case.noms_artistes), set(case.noms_artistes)
        periods1, periods2 = set(leaf_case.noms_periodes), set(case.noms_periodes)

        # Jaccard per artistes
        artist_similarity = len(artists1 & artists2) / len(artists1 | artists2) if artists1 | artists2 else 0
        artist_distance = 1 - artist_similarity

        # Jaccard per periodes
        period_similarity = len(periods1 & periods2) / len(periods1 | periods2) if periods1 | periods2 else 0
        period_distance = 1 - period_similarity

        # Distància per edat (normalitzada)
        age_distance = abs(leaf_case.edat - case.edat) / max(leaf_case.edat, case.edat)

        # Distància per hores (normalitzada)
        time_distance = abs(leaf_case.temps - case.temps) / max(leaf_case.temps, case.temps)

        # Combinar artistes, periodes, edat i hores segons els pesos
        combined_distance = (
            artist_distance * self.artist_weight +
            period_distance * self.period_weight +
            age_distance * self.age_weight +
            time_distance * self.time_weight
        ) / (self.artist_weight + self.period_weight + self.age_weight + self.time_weight)

        return combined_distance

    def retrieve(self, case):
        """
        Busca els 5 casos més propers en el sistema de casos, considerant artistes, periodes, edat i
        hores.
        """
        leaf_cases = self.arbre.fetch(case)  # Recuperem tots els casos de la fulla
        if len(leaf_cases) == 0:
            return []
        else:
            # Calcular distàncies per a tots els casos de les fulles
            distances = [
                (leaf_case, self.calculate_distance(case, leaf_case))
                for leaf_case in leaf_cases
            ]

            # Ordenar els casos per distància (de menor a major)
            distances.sort(key=lambda x: x[1])

            # Seleccionar els 5 millors casos
            top_cases = distances[:5]

            # Retornar els millors casos
            return top_cases

    def reuse(self, casospropers, case):
        """
        Adapta la informació del cas recuperat per crear una solució inicial pel nou cas.
        """
        # Prioritzar preferències
        recomanacio = obres.Artista.isin(case.noms_artistes)
        recomanacio |= obres.Periode.isin(case.noms_periodes)
        recomanacio = recomanacio.to_numpy()

        temps_acumulat = obres[recomanacio].Temps.sum()

        # Agafar obres dels casos propers
        punts_obres = np.zeros(obres.shape[0])
        for cas_prop, dist in casospropers:
            pes = cas_prop.valoracio * 2 - 1 # Passar a [-1, 1]
            pes = pes * dist
            puntuacions = np.isin(obres.Titol, cas_prop.noms_obres) * pes
            punts_obres += puntuacions

        # Softmax
        probs_obres = np.exp(punts_obres - punts_obres.max())
        probs_obres /= probs_obres.sum()

        probs_obres[recomanacio] = 0.
        probs_obres /= probs_obres.sum()

        while temps_acumulat < case.temps and recomanacio.sum() > obres.shape[0]:
            o = random.choices(range(obres.shape[0]), probs_obres)[0]
            recomanacio[o] = True
            probs_obres[o] = 0.
            probs_obres /= probs_obres.sum()
            temps_acumulat += obres.iloc[o].Temps

        case.obres = recomanacio

    def retain(self, cas):
        """
        Emmagatzema el nou cas i la seva solució al sistema de casos.
        """
        tots_casos = self.arbre.recorre_fulles()
        v25, v75 = np.percentile([cas.valoracio for cas in tots_casos], [25, 75])
        if cas.valoracio < v25 or cas.valoracio > v75:
            self.arbre.feed(cas)


    def __call__(self, case):
        """
        Implementa tot el cicle CRB per un cas donat.
        """
        # 1. Retrieve
        top_cases = self.retrieve(case)

        # 2. Reuse
        self.reuse(top_cases, case)

        # 3. Valorar
        valorar(case)

        # 4. Retain
        self.retain(case)
