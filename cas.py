import json
import numpy as np

path_domini = "data/domini.json"

class Cas:
    def __init__(self, nombre: int, edat: int, hores: int, dies: int,
                 autors: list[str] = [], estils: list[str] = []):
        """
        - nombre: int[1,  15]
        - edat (mitjana): int[0, 100]
        - hores: int[1,  12]
        - dies: int[1,   5]
        - autors: list[str]
        - estils: list[str]
        
        Per construir els vectors binaris s'utilitza el fitxer data/domini.json.
        Els autors i estils mai vistos s'afegiran (i per tant la mida dels
        vetors augmentarà).
        Intentem no fer innecessàriament gran el domini de moment.
        """

        assert all(isinstance(x, int) for x in [nombre, edat, hores, dies])
        assert all(isinstance(x, list) for x in [autors, estils])
        assert all(isinstance(x, str) for x in autors + estils)

        self.nombre = nombre
        self.edat = edat
        self.hores = hores
        self.dies = dies
        self.autors = autors
        self.estils = estils
        self.obres = None

        with open(path_domini) as f:
            domini = json.load(f)
        
        autors = set(autors)
        autorsD = set(domini["autors"])
        if not autors <= autorsD:
            domini["autors"].extend([a for a in autors if a not in autorsD])

        estils = set(estils)
        estilsD = set(domini["estils"])
        if not estils <= estilsD:
            domini["estils"].extend([e for e in estils if e not in estilsD])
        
        with open(path_domini, 'w') as f:
            json.dump(domini, f)

    def recomanar(self, obres: list[str]) -> None:
        """
        Ens interessa més assignar-les com una llista d'strings o com el vector
        binari??
        Ja ho cambiarem

        Per construir els vectors binaris s'utilitza el fitxer data/domini.json.
        Les obres mai vistos s'afegiran (i per tant la mida dels
        vetors augmentarà).
        Intentem no fer innecessàriament gran el domini de moment.
        """

        assert isinstance(obres, list)
        assert all(isinstance(x, str) for x in obres)

        self.obres = obres

        with open(path_domini) as f:
            domini = json.load(f)

        obres = set(obres)
        obresD = set(domini["obres"])
        if not obres <= obresD:
            domini["obres"].extend([e for e in obres if e not in obresD])
        
        with open(path_domini, 'w') as f:
            json.dump(domini, f)

    def array_feats(self) -> np.ndarray:
        """
        Retorna el vector dels 4 atributs "nombre", "edat", "hores" i "dies";
        seguit dels dos vectors binaris per "autors" i "estils"
        """

        atributs = np.array([self.nombre, self.edat, self.hores, self.dies])

        with open(path_domini) as f:
            domini = json.load(f)
        
        autors = np.isin(domini["autors"], self.autors).astype(int)
        estils = np.isin(domini["estils"], self.estils).astype(int)
        
        return np.concat([atributs, autors, estils])

    def array_obres(self) -> np.ndarray:
        """
        Retorna el vector binari per les obres recomanades
        """

        with open(path_domini) as f:
            domini = json.load(f)
        
        return np.isin(domini["obres"], self.obres).astype(int)