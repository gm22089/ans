
import sympy as sp
import re
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
            if valorActual == valorAnterior:
                return {"error": "Error\nNo se puede hacer ek valor porcentual."}
            errorP = sp.Abs((valorActual-valorAnterior)/valorActual) * 100
            return float(errorP)
        except Exception as e:
            return {f"error": "Error inesperado: {e}"}

    @staticmethod
    def latex_(latex):
        if not latex or not isinstance(latex, str) or not latex.strip():
            return {"error": "Debe ingresar una ecuación válida (no vacía)."}

        try:
            importlib.reload(importlib.import_module('latex2sympy2'))
            latex = re.sub(r'(?<!\\)[A-Z]', lambda m: m.group().lower(), latex)
            funcion = expand(latex2sympy(latex))

            # Validamos que solo use la variable 'x'
            variables = funcion.free_symbols
            if not variables or any(str(var) != 'x' for var in variables):
                return {"error": "La ecuación debe contener únicamente la variable 'x'."}

            f = sp.lambdify(sp.Symbol('x'), funcion, modules=["math"])
            return {"ok": {"funcion": funcion, "f": f}}

        except Exception as e:
            return {"error": f"Ecuación inválida. Detalles: {str(e)}"}

    @staticmethod
    def validarNumero(dato, nombre="dato"):
        if dato is None or (isinstance(dato, str) and not dato.strip()):
            return {"error": f"El valor de {nombre} debe de ser un numero valido."}
        try:
            numero = float(dato)
            return {"ok": numero}
        except:
            return {"error": f"El {nombre} debe de ser un numero valido."}

    @staticmethod
    def validarTolerancia(tolerenciaRecinida):
        resultado = Utilidades.validarNumero(tolerenciaRecinida, "tolerancia")
        if "error" in resultado:
            return resultado
        if resultado["ok"] <= 0:
            return {"error": "La tolerancia debe ser un número mayor que cero."}
        else:
            return {"ok": resultado["ok"]}

    @staticmethod
    def evaluarPunto(f, punto):
        """
        Evalúa la función f en el punto dado y valida si se vuelve infinita, indefinida o cero.

        :param f: función ya lambdificada
        :param punto: valor numérico (float o int)
        :return: dict con clave 'ok' si la evaluación fue exitosa, o 'error' si hubo un problema
        """
        try:
            resultado = f(punto)

            if resultado is None:
                return {"error": f"La función no pudo evaluarse en x = {punto} (resultado None)."}

            if isinstance(resultado, complex):
                return {"error": f"La función devuelve un número complejo en x = {punto}: {resultado}"}

            if isinstance(resultado, (int, float)):
                if resultado == 0:
                    return {"ok": 0}  # o puedes marcar como error si lo deseas
                elif resultado == float('inf') or resultado == float('-inf'):
                    return {"error": f"La función tiende a infinito en x = {punto}."}
                elif resultado != resultado:  # NaN se evalúa a falso en comparación consigo mismo
                    return {"error": f"La función devuelve un valor indefinido (NaN) en x = {punto}."}
                else:
                    return {"ok": resultado}

            return {"error": f"No se pudo interpretar el resultado en x = {punto}: {resultado}"}

        except ZeroDivisionError:
            return {"error": f"División entre cero al evaluar la función en x = {punto}."}
        except Exception as e:
            return {"error": f"Error inesperado al evaluar la función en x = {punto}: {e}"}

    @staticmethod
    def validarIntervalos(a, b):
        if a >= b:
            return {"error": "El limite inferior debe ser menor que el limite superior"}
        return {"ok": True}
