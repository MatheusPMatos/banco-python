import math
import unittest
from forma import Circulo, Retangulo  # supondo que o código original esteja em formas.py

class TestFormas(unittest.TestCase):
    def test_area_circulo(self):
        c = Circulo(raio=10)
        resultado = c.area()
        esperado = math.pi * 10**2
        self.assertAlmostEqual(resultado, esperado, places=5)

    def test_area_retangulo(self):
        r = Retangulo(alt=5, largura=8)
        resultado = r.area()
        esperado = 5 * 8
        self.assertEqual(resultado, esperado)

    def test_area_circulo_zero(self):
        c = Circulo(raio=0)
        self.assertEqual(c.area(), 0)

    def test_area_retangulo_negativo(self):
        r = Retangulo(alt=-2, largura=3)
        resultado = r.area()
        self.assertEqual(resultado, -6)  # comportamento atual


if __name__ == '__main__':
    unittest.main()
