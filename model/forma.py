import math
from abc import ABC, abstractmethod
from singleton import singleton
class Forma(ABC):
    @abstractmethod
    def area(self):
        pass

class Circulo(Forma):
    def __init__(self, raio):
        self.raio = raio
    def area(self):
        return math.pow(self.raio, 2) * math.pi


class Retangulo(Forma):
    def __init__(self, alt: float, largura: float):
        self.altura = alt
        self.largura = largura
    def area(self):
        return self.altura * self.largura

@singleton
class Logger:
    def warn(self, msg: str):
        print(f"[WARN] {msg}")

    def error(self, msg: str):
        print(f"[ERROR] {msg}")