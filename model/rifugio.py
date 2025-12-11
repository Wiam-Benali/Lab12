from dataclasses import dataclass

@dataclass
class Rifugio():
    id : int
    nome : str
    localita: str

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f'[{self.id}] {self.nome} ({self.localita})'

    def __eq__(self, other):
        return self.id == other.id