import json
import numpy as np

path_domini = "dades/domini.json"

class Cas:
    def __init__(self, nombre: int, edat: int, hores: int, dies: int, tipus: int, valoracio: int,
                 artistes: list[str] = [], periodes: list[str] = [], force: bool = False):
        """
        - nombre: int[1,  15]
        - edat (mitjana): int[0, 100]
        - hores: int[1,  12]
        - dies: int[1,   5]
        - artistes: list[str]
        - periodes: list[str]
        
        Per construir els vectors binaris s'utilitza el fitxer data/domini.json.
        Els artistes i periodes mai vistos s'afegiran (i per tant la mida dels vetors augmentarà).
        Intentem no fer innecessàriament gran el domini de moment.
        """

        assert all(isinstance(x, int) for x in [nombre, edat, hores, dies, tipus, valoracio])
        assert all(isinstance(x, list) for x in [artistes, periodes])
        assert all(isinstance(x, str) for x in artistes + periodes)

        self.nombre = nombre
        self.edat = edat
        self.hores = hores
        self.dies = dies
        self.tipus = tipus
        self.artistes = artistes
        self.periodes = periodes
        self.valoracio = valoracio
        self.obres = None

        with open(path_domini) as f:
            domini = json.load(f)
        
        artistes = set(artistes)
        artistesD = set(domini["artistes"])
        if not artistes <= artistesD:
            if force or input(
                f"Aquests artistes {artistes - artistesD} encara no estan al domini. "
                "Vols afegir-los? [si]"
            ) == 'si':
                domini["artistes"].extend([a for a in artistes if a not in artistesD])
            else:
                raise Exception("Artistes fora el domini")

        periodes = set(periodes)
        periodesD = set(domini["periodes"])
        if not periodes <= periodesD:
            if force or input(
                f"Aquests periodes {periodes - periodesD} encara no estan al domini. "
                "Vols afegir-los? [si]"
            ) == 'si':
                domini["periodes"].extend([e for e in periodes if e not in periodesD])
            else:
                raise Exception("Periodes fora el domini")
        
        with open(path_domini, 'w') as f:
            json.dump(domini, f)

    def recomanar(self, obres: list[str], force: bool = False) -> None:
        """
        Ens interessa més assignar-les com una llista d'strings o com el vector binari??
        Ja ho cambiarem

        Per construir els vectors binaris s'utilitza el fitxer data/domini.json.
        Les obres mai vistos s'afegiran (i per tant la mida dels vectors augmentarà).
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
            if force or input(
                f"Aquestes obres {obres - obresD} encara no estan al "
                "domini, vols afegir-les? [si]"
            ) == 'si':
                domini["obres"].extend([e for e in obres if e not in obresD])
            else:
                raise Exception("Obres fora el domini")
        
        with open(path_domini, 'w') as f:
            json.dump(domini, f)

    def array_feats(self) -> np.ndarray:
        """
        Retorna el vector dels 4 atributs "nombre", "edat", "hores" i "dies"; seguit dels dos
        vectors binaris per "artistes" i "periodes"
        """

        atributs = np.array([self.nombre, self.edat, self.hores, self.dies, self.tipus, self.valoracio])

        with open(path_domini) as f:
            domini = json.load(f)
        
        artistes = np.isin(domini["artistes"], self.artistes).astype(int)
        periodes = np.isin(domini["periodes"], self.periodes).astype(int)
        
        return np.concat([atributs, artistes, periodes])

    def array_obres(self) -> np.ndarray:
        """
        Retorna el vector binari per les obres recomanades
        """

        with open(path_domini) as f:
            domini = json.load(f)
        
        return np.isin(domini["obres"], self.obres).astype(int)