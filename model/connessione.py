from dataclasses import dataclass

@dataclass
class Conessione():
    id : int
    id1 : int
    id2 : int
    distanza : float
    difficolta: str
    peso = 0


    def calcola_peso(self):
        fattore_difficoltà = 0
        if self.difficolta == 'facile':
            fattore_difficoltà = 1
        elif self.difficolta == 'media':
            fattore_difficoltà = 1.5
        elif self.difficolta == 'difficile':
            fattore_difficoltà = 2

        self.peso = float(self.distanza)*fattore_difficoltà