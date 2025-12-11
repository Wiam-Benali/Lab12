import copy
import math

import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.G = nx.Graph()
        self._nodes = None
        self._edges = None
        self._pesi_archi = []

        # attributi x ricorsione
        self._percorso_ottimale = []
        self._peso_ottimale = 0

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        self.G.clear()
        self._nodes = DAO.read_all_rifugi(year)
        self._edges = DAO.read_all_conessioni(year)

        self.G.add_nodes_from(self._nodes.values())

        for edge in self._edges:
            edge.calcola_peso()  # peso = guadagno medio per spedizione)
            self._pesi_archi.append(edge.peso)
            nodo1 = self._nodes[edge.id1]
            nodo2 = self._nodes[edge.id2]
            self.G.add_edge(nodo1,nodo2, weight=edge.peso)

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        return min(self._pesi_archi),max(self._pesi_archi)


    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        count_archi_magg_soglia = 0
        count_archi_min_soglia = 0
        for peso in self._pesi_archi:
            if peso > soglia:
                count_archi_magg_soglia += 1
            elif peso < soglia:
                count_archi_min_soglia += 1
        return count_archi_min_soglia, count_archi_magg_soglia


    """Implementare la parte di ricerca del cammino minimo"""

    def ricerca_cammino_minimo(self, s):
        self._percorso_ottimale = []
        self._peso_ottimale = [math.inf]
        # salvo il peso ottimale come lista in modo da salvarmi i pesi di ciascun arco
        for nodo in self.G.nodes():
            self.ricorsione([nodo], [], s)
        return self._percorso_ottimale,self._peso_ottimale


    def ricorsione(self, percorso, peso_corrente, s):

        if len(percorso) >= 3:
            if sum(peso_corrente) < sum(self._peso_ottimale):
                self._percorso_ottimale = copy.deepcopy(percorso)
                self._peso_ottimale = copy.deepcopy(peso_corrente)
        nodo_attuale = percorso[-1]

        for vicino in self.G.neighbors(nodo_attuale):
            if vicino not in percorso:
                dati_arco = self.G.get_edge_data(nodo_attuale, vicino)
                peso_arco = dati_arco.get('weight', 1)
                if peso_arco > s:
                    peso_corrente.append(peso_arco)

                    if sum(peso_corrente) < sum(self._peso_ottimale): # senza questa ottimizzazione ci mette troppo
                        percorso.append(vicino)
                        self.ricorsione(percorso, peso_corrente, s)
                        percorso.pop()
                        peso_corrente.pop()





