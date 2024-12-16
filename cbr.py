import numpy as np
from base_casos import Node
import json
import random

path_domini = "dades/domini.json"

class CBR:
    def __init__(self, root, artist_weight=1.0, period_weight=1.0, age_weight=1.0, hours_weight=1.0):
        """
        Inicialitza el sistema amb l'arrel i els pesos per artistes, periodes, edat i hores.
        """
        self.root = root
        self.artist_weight = artist_weight
        self.period_weight = period_weight
        self.age_weight = age_weight
        self.hours_weight = hours_weight

    def calculate_distance(self, case, leaf_case):
        """
        Calcula la distància entre dos casos, considerant artistes, periodes, edat i hores.
        """
        # Distància numèrica ponderada
        numeric_distance = np.sqrt(np.sum((leaf_case.to_array() - case.to_array()) ** 2))

        # Distància conjunta per artistes i periodes (Jaccard combinada)
        artists1, artists2 = set(leaf_case.artistes), set(case.artistes)
        periods1, periods2 = set(leaf_case.periodes), set(case.periodes)

        # Jaccard per artistes
        artist_similarity = len(artists1 & artists2) / len(artists1 | artists2) if artists1 | artists2 else 0
        artist_distance = 1 - artist_similarity

        # Jaccard per periodes
        period_similarity = len(periods1 & periods2) / len(periods1 | periods2) if periods1 | periods2 else 0
        period_distance = 1 - period_similarity

        # Distància per edat (normalitzada)
        age_distance = abs(leaf_case.edat - case.edat) / max(leaf_case.edat, case.edat)

        # Distància per hores (normalitzada)
        hours_distance = abs(leaf_case.hores - case.hores) / max(leaf_case.hores, case.hores)

        # Combinar artistes, periodes, edat i hores segons els pesos
        combined_distance = (
            artist_distance * self.artist_weight +
            period_distance * self.period_weight +
            age_distance * self.age_weight +
            hours_distance * self.hours_weight
        ) / (self.artist_weight + self.period_weight + self.age_weight + self.hours_weight)

        # Suma ponderada de les distàncies
        total_distance = numeric_distance + combined_distance
        return total_distance

    def retrieve(self, case):
        """
        Busca els 5 casos més propers en el sistema de casos, considerant artistes, periodes, edat i hores.
        """
        print("=== Retrieve ===")
        leaf_cases = self.root.feed(case)  # Recuperem tots els casos de la fulla
        if leaf_cases is None or len(leaf_cases) == 0:
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
            print("  -> Els 5 millors casos recuperats:")
            for i, (retrieved_case, dist) in enumerate(top_cases, 1):
                print(f"     {i}. Cas: {retrieved_case}, Distància: {dist:.4f}")

            # Retornar els 5 millors casos
            return top_cases

    def reuse(self, casospropers, case):
        """
        Adapta la informació del cas recuperat per crear una solució inicial pel nou cas.
        """
        print("\n=== Reuse ===")
        cas_recomanat =  []

        min_dist, max_dist = 0, max([dist for _, _, dist in casospropers])
        #Valoracio entenc que està entre -1 i 1

        a = 0.6  #VAL
        b = 0.4  #DIST (x exemple)

        pesos_casos = []
        for valoracio, dist in casospropers:
            dist_norm = 1 - (max_dist - dist) / (max_dist - min_dist)
            
            pes_cas = a* valoracio + b*dist_norm
            pesos_casos.append(pes_cas)

        puntuacio_obres = []
        for case, pes_cas in pesos_casos:
            for obra in case.obres:
                if obra not in cas_recomanat:
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

        while len(cas_recomanat) < 10:
            obra_seleccionada = random.choices([obra for obra, _ in probs_obres_norm], weights=[pes for _, pes in probs_obres_norm], k=1)[0]
        cas_recomanat.append(obra_seleccionada)


        if case.artistes in domini['artistes']:
            for artista in
            obres = [obra for obra in domini["obres"]
            if any(artista in artistes_a_afegir for artista in case.artistes) or
    
        ]
        


        #MODIFICA OBRES SEGONS PREFERENCIA(DE MOMENT SIMPLE)
        obres_cas_proper = set(closest_case.obres)
        artistes_a_eliminar = set(closest_case.artistes) - set(case.artistes)
        artistes_a_afegir = set(case.artistes) - set(closest_case.artistes)
        periodes_a_eliminar = set(closest_case.periodes) - set(case.periodes)
        periodes_a_afegir = set(case.periodes) - set(closest_case.periodes)

        obres_a_eliminar = [
            obra for obra in obres_cas_proper
            if any(artista in artistes_a_eliminar for artista in closest_case.artistes) or
            any(periode in periodes_a_eliminar for periode in closest_case.periodes)
        ]
        obres_adaptades = obres_cas_proper - set(obres_a_eliminar)
        with open("dades/domini.json") as f:
            domini = json.load(f)
        obres_a_afegir = [
            obra for obra in domini["obres"]
            if any(artista in artistes_a_afegir for artista in case.artistes) or
            any(periode in periodes_a_afegir for periode in case.periodes)
        ]
        recom_adaptada = obres_adaptades.union(obres_a_afegir)

 

            #Saber preferencies del nou cas

            #ADAPTAR DIFERENCIES
            #SI SON + GENT, + HORES O DIFERENT EDAT -> CANVIAR TEMPS/ ADAPTAR OBRES VISTES
            #PREFERENCIES DIFERENTS -> AFEGIR OBRES PREFERENCIA , ELIMINAR OBRES NO PREFERENCIA???
        print(f"  -> Solució inicial: {solution}")
        return recom_adaptada

    def revise(self, solution):
        """
        Revisa la solució proposada. Aquí se simula una revisió manual o automàtica.
        """
        print("\n=== Revise ===")
        # Simulem una revisió manual o automàtica
        revised_solution = solution.copy()
        revised_solution["revised"] = True  # Marquem la solució com revisada
        print(f"  -> Solució revisada: {revised_solution}")
        return revised_solution

    def retain(self, case, solution):
        """
        Emmagatzema el nou cas i la seva solució al sistema de casos.
        """
        print("\n=== Retain ===")
        print(f"  -> Emmagatzemant el cas {case} amb la solució {solution}.")
        self.root.feed(case)  # El nou cas es guarda al sistema de nodes

    def crb(self, case):
        """
        Implementa tot el cicle CRB per un cas donat.
        """
        # 1. Retrieve
        closest_case = self.retrieve(case)

        # 2. Reuse
        solution = self.reuse(closest_case, case)

        # 3. Revise
        revised_solution = self.revise(solution)

        # 4. Retain
        self.retain(case, revised_solution)

        print("\n=== CRB Finalitzat ===")
        return revised_solution