from sympy import sympify, expand, printing
from latex2sympy2 import latex2sympy
import sympy
from flask import jsonify
from app.unidad2.utilidades.utils import Utilidades


def biseccion(ecuacion, a, b, tolerancia):
    errorP = Utilidades()
    ecuacionR = Utilidades()
    x = sympy.symbols('x')

    try:
        funcion = ecuacionR.latex_(ecuacion)
        print(funcion)
        f = sympy.lambdify(x, funcion)
    except Exception as e:
        return jsonify({"error": f"Error en la ecuación: {e}"})
    except ZeroDivisionError:
        return jsonify({"error": "La división entre cero da infinito. Verifique su denominador."})
    except sympy.SympifyError:
        return jsonify({"error": "Error en la sintaxis de su ecuación."})

    if f(a) * f(b) >= 0:
        return jsonify({"error": "El intervalo no es válido. La función debe cambiar de signo en el rango dado."})

    Xi = a
    X2 = b
    Xr = (Xi + X2) / 2
    anterior = 0
    resultados = []

    for i in range(20):
        Ea = errorP.errorPorcentual(Xr, anterior) if i > 0 else None

        try:
            Fi = f(Xi)
            F2 = f(Xr)
        except Exception as e:
            return jsonify({"error": f"Error en la evaluación de la función: {e}"})

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

        if Ea is not None and Ea < tolerancia:
            break

        if Fi * F2 < 0:
            X2 = Xr
        else:
            Xi = Xr

        anterior = Xr
        Xr = (Xi + X2) / 2

    return jsonify(resultados)
