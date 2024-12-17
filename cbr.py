import numpy as np
from generador import valorar
import json
import random
import pandas as pd

with open("dades/domini.json") as f:
    domini = json.load(f)

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
        print("=== Retrieve ===")
        leaf_cases = self.arbre.fetch(case)  # Recuperem tots els casos de la fulla
        if len(leaf_cases) == 0:
            print("  -> No s'ha trobat cap cas similar (nou cas).")
            return None
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

            # Mostrar resultats
            print(f"  -> Els {len(top_cases)} millors casos recuperats:")
            for i, (retrieved_case, dist) in enumerate(top_cases, 1):
                print(f"     {i}. Cas: {retrieved_case}, Distància: {dist:.4f}")

            # Retornar els millors casos
            return top_cases

    def reuse(self, casospropers, case):
        """
        Adapta la informació del cas recuperat per crear una solució inicial pel nou cas.
        """
        print("\n=== Reuse ===")
        cas_recomanat =  []

        min_dist, max_dist = 0, max([dist for _, dist in casospropers])
        #Valoracio entenc que està entre -1 i 1

        a = 0.6  #VAL
        b = 0.4  #DIST (x exemple)

        puntuacio_obres = []
        for c, dist in casospropers:
            dist_norm = 1 - (max_dist - dist) / (max_dist - min_dist)
            
            pes_cas = a* c.valoracio + b*dist_norm
            for obra in c.obres:
                if obra not in puntuacio_obres:
                    puntuacio_obres[obra] = {"pos": 0, "neg": 0}
                if pes_cas > 0:
                    puntuacio_obres[obra]["pos"] += pes_cas
                else:
                    puntuacio_obres[obra]["neg"] += abs(pes_cas)
            

        probs_obres = []
        for obra,scores in puntuacio_obres.items():
            pesf = scores["pos"] - scores["neg"]
            probs_obres.append((obra, pesf))

        min_pes = min(pes for _, pes in probs_obres)
        if min_pes < 0:
            probs_obres_norm = [(obra, pes - min_pes) for obra, pes in probs_obres]

        while cas_recomanat.temps < case.temps:
            obra_seleccionada = random.choices([obra for obra, _ in probs_obres_norm], weights=[pes for _, pes in probs_obres_norm], k=1)[0]
        cas_recomanat.append(obra_seleccionada)

        obres = pd.read_csv("dades/obres.csv")
        tempo = 0
        if any(artista in domini['artistes'] for artista in case.noms_artistes):
            obres_pref = []
            for _, obra in obres.iterrows(): 
                if obra['Artista'] in case.noms_artistes: 
                    obres_pref.append(obra)
                    tempo += obra['Temps']
            while tempo > 0:
                obra_treure = cas_recomanat.pop()
                tempo -= obra_treure['Temps']
            for obra in obres_pref:
                cas_recomanat.append(obra)

        tempo2 = 0
        if any(periode in domini['periodes'] for periode in case.noms_periodes):
            obres_pref2 = []
            for _, obra in obres.iterrows(): 
                if obra['Periode'] in case.noms_periodes: 
                    obres_pref2.append(obra)
                    tempo2 += obra['Temps']
            
        while tempo2 > 0 and cas_recomanat: 
            obra_treure = cas_recomanat[-1] 
            if obra_treure['Artista'] in case.noms_artistes:
                cas_recomanat = cas_recomanat[:-1] + [obra_treure]
                continue
            cas_recomanat.pop()  
            tempo2 -= obra_treure['Temps']
            for obra in obres_pref2:
                cas_recomanat.append(obra)

        

        print(f" Cas recomanat: {cas_recomanat}")
        return cas_recomanat

    def retain(self, case, solution):
        """
        Emmagatzema el nou cas i la seva solució al sistema de casos.
        """
        print("\n=== Retain ===")
        valorar(solution)
        #extreure valoracions
        tots_casos = self.root.recorre_fulles()
        total_casos = len(tots_casos)
        valoracions = [cas.valoracio for cas in tots_casos]
        mitjana = sum(valoracions) / total_casos
        interval_5 = 0.1 * mitjana
        valoracio = solution.valoracio
<<<<<<< HEAD
        
        if valoracio < (mitjana - interval_5) or valoracio > (mitjana + interval_5):
            self.root.feed(case) 
                    


    def crb(self, case):
        """
        Implementa tot el cicle CRB per un cas donat.
        """
        # 1. Retrieve
        top_cases = self.retrieve(case)

        # 2. Reuse
        solution = self.reuse(top_cases, case)

        # 3. Revise
        revised_solution = self.revise(solution)

        # 4. Retain
        self.retain(case, revised_solution)

        print("\n=== CRB Finalitzat ===")
        return revised_solution
=======
        if valoracio > 0.6 and valoracio < 0.4:
            self.root.feed(case)
>>>>>>> 5ddf582af24e5d5b365c796a2653863d3b2f3cf1
