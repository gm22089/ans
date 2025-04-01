import numpy as np
from sympy import sympify
from flask import jsonify
import sympy
from app.unidad2.utilidades.utils import Utilidades


def falsaPosicion(ecuacion, a, b, tolerancia):

    errorP = Utilidades()
    ecuacionR = Utilidades()
    Ea = 0
    X1 = a
    X2 = b
    i = 0
    anterior = 0
    resultado = []
    x = sympy.symbols('x')
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

    Xr = X2 - ((f(X2) * (X1 - X2)) / (f(X1) - f(X2)))

    for i in range(20):
        Ea = errorP.errorPorcentual(Xr, anterior) if i > 0 else None

        try:
            Fi = f(X1)  # Evaluar la función en Xi
            F2 = f(Xr)  # Evaluar la función en Xr
        except Exception as e:
            return jsonify({"error": f"Error en la evaluación de la función: {e}"})

        resultado.append({
            "iteracion": i + 1,
            "Xi": round(X1, 6),
            "X2": round(X2, 6),
            "Xr": round(Xr, 6),
            "fXi": round(Fi, 6),
            "fX2": round(f(X2), 6),
            "fXr": round(F2, 6),
            "error": "-----" if Ea is None else round(Ea, 6)
        })
        anterior = Xr
        # Método de bisección correctamente aplicado
        if Fi * F2 < 0:
            X2 = Xr  # La raíz está en [Xi, Xr]
        else:
            X1 = Xr  # La raíz está en [Xr, X2]
        if Ea is not None and Ea < tolerancia:
            break

        Xr = X2 - ((f(X2) * (X1 - X2)) / (f(X1) - f(X2)))

    return jsonify(resultado)
