import sympy as sp
from app.unidad2.utilidades.utils import Utilidades
from flask import jsonify


def puntoFijo(ecuacion, a, tolerancia):
    x = sp.Symbol('x')

    utilidad = Utilidades()
    resultados = []
    try:
        funcion = utilidad.latex_(ecuacion)
        f = sp.lambdify(x, funcion)
    except ZeroDivisionError:
        return jsonify({"error": "La división entre cero da infinito. Verifique su denominador."})
    except sp.SympifyError:
        return jsonify({"error": "Error en la sintaxis de su ecuación."})
    except Exception as e:
        return jsonify({"error": f"Error en la ecuación: {e}"})

    Xi = a

    print("Iteracion\tXi\t\tF(xi)\t\tEa %\n")
    for i in range(20):

        Xr = f(Xi)+Xi

        Ea = utilidad.errorPorcentual(Xr, Xi)
        print(f"{i+1:.8f}\t{Xi:.8f}\t{Xr:.8f}\t{Ea:.8f}")
        resultados.append({
            "iteracion": i+1,
            "xi": round(Xi, 6),
            "fXi": round(f(Xi) + Xi, 6),
            "error": "-----" if Ea is None else round(Ea, 6)
        })
        Xi = Xr
        if Ea < tolerancia:
            break

    return jsonify(resultados)
