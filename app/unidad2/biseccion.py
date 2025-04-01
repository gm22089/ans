from sympy import sympify, expand, printing
from latex2sympy2 import latex2sympy
import sympy
from flask import jsonify
from app.unidad2.utilidades.utils import Utilidades


def biseccion(ecuacion, a, b, tolerancia):
    """
    Implementa el método de bisección para encontrar la raíz de una ecuación.

    :param ecuacion: Ecuación en formato LaTeX.
    :param a: Límite inferior del intervalo.
    :param b: Límite superior del intervalo.
    :param tolerancia: Tolerancia aceptable para el error porcentual.
    :return: JSON con los resultados de cada iteración o mensaje de error.
    """

    # Crear instancias de la clase Utilidades para cálculos de error y manejo de ecuaciones
    errorP = Utilidades()
    ecuacionR = Utilidades()
    x = sympy.symbols('x')  # Definir el símbolo 'x' para la ecuación

    try:
        # Convertir la ecuación en formato LaTeX a una función interpretable por SymPy
        funcion = ecuacionR.latex_(ecuacion)
        print(funcion)  # Mostrar la ecuación convertida en consola para depuración
        # Convertir la ecuación en una función evaluable
        f = sympy.lambdify(x, funcion)
    except ZeroDivisionError:
        return jsonify({"error": "La división entre cero da infinito. Verifique su denominador."})
    except sympy.SympifyError:
        return jsonify({"error": "Error en la sintaxis de su ecuación."})
    except Exception as e:
        return jsonify({"error": f"Error en la ecuación: {e}"})

    # Verificar que la función cambia de signo en el intervalo dado
    if f(a) * f(b) >= 0:
        return jsonify({"error": "El intervalo no es válido. La función debe cambiar de signo en el rango dado."})

    # Inicializar variables del método de bisección
    Xi = a  # Extremo izquierdo del intervalo
    X2 = b  # Extremo derecho del intervalo
    Xr = (Xi + X2) / 2  # Punto medio del intervalo
    anterior = 0  # Valor previo de Xr para calcular error
    resultados = []  # Lista para almacenar los resultados de cada iteración

    for i in range(20):  # Máximo de 20 iteraciones
        # Calcular error porcentual en iteraciones posteriores a la primera
        Ea = errorP.errorPorcentual(Xr, anterior) if i > 0 else None

        try:
            Fi = f(Xi)  # Evaluar la función en Xi
            F2 = f(Xr)  # Evaluar la función en Xr
        except Exception as e:
            return jsonify({"error": f"Error en la evaluación de la función: {e}"})

        # Guardar los resultados de la iteración actual
        resultados.append({
            "iteracion": i + 1,
            "Xi": round(Xi, 6),
            "X2": round(X2, 6),
            "Xr": round(Xr, 6),
            "fXi": round(Fi, 6),
            "fX2": round(f(X2), 6),
            "fXr": round(F2, 6),
            "error": "-----" if Ea is None else round(Ea, 6)
        })

        # Si el error es menor que la tolerancia, detener la iteración
        if Ea is not None and Ea < tolerancia:
            break

        # Actualizar el intervalo según el método de bisección
        if Fi * F2 < 0:
            X2 = Xr  # La raíz está en la izquierda del intervalo
        else:
            Xi = Xr  # La raíz está en la derecha del intervalo

        anterior = Xr  # Guardar el valor de Xr anterior
        Xr = (Xi + X2) / 2  # Calcular nuevo Xr como el punto medio

    return jsonify(resultados)  # Devolver resultados en formato JSON
