
import sympy as sp
from sympy import expand, printing
from latex2sympy2 import latex2sympy
import importlib


class Utilidades:
    def __init__(self):
        self.x = sp.Symbol('x')

    def primeraDerivada(self, ecuacion):
        try:
            funcion = sp.sympify(ecuacion)
            primerDx = sp.diff(funcion, self.x)
            # Se transforma en str para utilizarla como JSON
            return str(primerDx)
        except ZeroDivisionError:
            return ("La division entre cero da infinito!!!\nNo somos capaces de calcular el infinito\nPor favor verefique su denominador")
        except sp.SympifyError:
            return ('Error.\nVerefique la sintaxis de su ecuacion')
        except Exception as e:
            return ('Huy!!!\nError inesperado...')

    def segundaDerivada(self, ecuacion):
        try:
            funcion = sp.sympify(ecuacion)
            segundaDx = sp.diff(funcion, self.x, 2)
            # Se transforma en str para utilizarla como JSON
            return str(segundaDx)
        except ZeroDivisionError:
            return ("La division entre cero da infinito!!!\nNo somos capaces de calcular el infinito\nPor favor verefique su denominador")
        except sp.SympifyError:
            return ('Error.\nVerefique la sintaxis de su ecuacion')
        except Exception as e:
            return ('Huy!!!\nError inesperado...')

    @staticmethod
    def errorPorcentual(valorActual, valorAnterior):
        try:
            if valorActual == 0:
                return "Error\nEl valor actual no puede ser cero."
            errorP = sp.Abs((valorActual-valorAnterior)/valorActual) * 100
            return float(errorP)
        except Exception as e:
            return f"Error inesperado: {e}"

    @staticmethod
    def latex_(latex):
        importlib.reload(importlib.import_module('latex2sympy2'))
        return expand(latex2sympy(latex))
