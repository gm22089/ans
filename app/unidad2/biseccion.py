from sympy import sympify, expand, printing
from latex2sympy2 import latex2sympy
import sympy
from flask import jsonify
from app.unidad2.utilidades.utils import Utilidades


def biseccion(ecuacion, a, b, tolerancia):
    """
    Aplica el método de bisección para encontrar una raíz de la función dada en formato LaTeX.

    :param ecuacion: Cadena LaTeX que representa la ecuación a resolver.
    :param a: Límite inferior del intervalo de búsqueda.
    :param b: Límite superior del intervalo de búsqueda.
    :param tolerancia: Error porcentual aceptable para detener el algoritmo.
    :return: Lista de resultados por iteración o mensaje de error en formato JSON.
    """

    utilidad = Utilidades()

    # Validar y convertir la ecuación de LaTeX a una función evaluable
    validarEcuacion = utilidad.latex_(ecuacion)
    if "error" in validarEcuacion:
        return jsonify({"error": validarEcuacion["error"]})
    funcion = validarEcuacion["ok"]["funcion"]
    f = validarEcuacion["ok"]["f"]
    print(f"El String de la ecuación modificada:\n{funcion}")

    # Validar el extremo izquierdo del intervalo (a)
    validarA = utilidad.validarNumero(a)
    if "error" in validarA:
        return jsonify({"error": validarA["error"]})
    Xi = validarA["ok"]

    # Validar el extremo derecho del intervalo (b)
    validarB = utilidad.validarNumero(b)
    if "error" in validarB:
        return jsonify({"error": validarB["error"]})
    X2 = validarB["ok"]

    # Validar que los extremos del intervalo no sean iguales
    validarIntervalos = utilidad.validarIntervalos(Xi, X2)
    if "error" in validarIntervalos:
        return jsonify({"error": validarIntervalos["error"]})

    # Validar la tolerancia
    validarTolerancia = utilidad.validarTolerancia(tolerancia)
    if "error" in validarTolerancia:
        return jsonify({"error": validarTolerancia["error"]})
    toleranciaValidada = validarTolerancia["ok"]

    # Verificar que haya un cambio de signo entre los extremos del intervalo
    if f(Xi) * f(X2) >= 0:
        return jsonify({"error": "El intervalo no es válido.\nLa función debe cambiar de signo en el rango dado."})

    Xr = (Xi + X2) / 2  # Punto medio inicial
    anterior = 0  # Para almacenar el valor anterior de Xr y calcular el error
    resultados = []  # Lista para almacenar los datos de cada iteración

    for i in range(30):  # Limitar a un máximo de 30 iteraciones
        if i + 1 == 30:
            return jsonify({"error": "El número de iteraciones ha excedido el límite permitido."})

        # Calcular el error porcentual relativo (excepto en la primera iteración)
        Ea = utilidad.errorPorcentual(Xr, anterior) if i > 0 else None

        # Evaluar la función en los extremos actuales
        evaluarPuntoA = utilidad.evaluarPunto(f, Xi)
        evaluarPuntoB = utilidad.evaluarPunto(f, Xr)
        if "error" in evaluarPuntoA:
            return jsonify({"error": evaluarPuntoA["error"]})
        if "error" in evaluarPuntoB:
            return jsonify({"error": evaluarPuntoB["error"]})

        Fi = evaluarPuntoA["ok"]
        F2 = evaluarPuntoB["ok"]

        # Guardar resultados de la iteración actual
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

        # Verificar si se ha alcanzado la tolerancia deseada
        if Ea is not None and Ea < toleranciaValidada:
            break

        # Actualizar el intervalo dependiendo del signo del producto f(Xi)*f(Xr)
        if Fi * F2 < 0:
            X2 = Xr
        else:
            Xi = Xr

        anterior = Xr
        Xr = (Xi + X2) / 2  # Nuevo punto medio

    return jsonify(resultados)
