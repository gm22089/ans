import numpy as np
from sympy import sympify
import sympy


def falsaPosicion(ecuacion, a, b, tolerancia):
    X1=a
    X2=b
    salirBucle=False
    Es=tolerancia
    i=0
    anterior=0
    Ea=1
    resultado=''
    x=sympy.symbols('x')
    try:
        funcion=sympify(ecuacion)
        resultado += "La funcion enviada es: " +ecuacion+"\n"
        print("La funcion enviada es:",funcion)
        
        f=sympy.lambdify(x, funcion)
    except Exception as e:
        return f"Error en la ecuacion: {e}"
    
    Xr = X2 - ((f(X2) * (X1 - X2)) / (f(X1) - f(X2)))

    resultado += "\nIteración\tX1\t\tX2\t\tXr\t\tf(X1)\t\tf(X2)\t\tf(Xr)\t\tError (%)\n"
    print("Iteración\tX1\t\tX2\t\tXr\t\tf(X1)\t\tf(X2)\t\tf(Xr)\t\tError (%)")

    while salirBucle==False:

        if i == 0:
            resultado += f"{i+1}\t\t{X1:.6f}\t{X2:.6f}\t{Xr:.6f}\t{f(X1):.6f}\t{f(X2):.6f}\t{f(Xr):.6f}\t-----\n"
            print(f"{i+1}\t\t{X1:.6f}\t{X2:.6f}\t{Xr:.6f}\t{f(X1):.6f}\t{f(X2):.6f}\t{f(Xr):.6f}\t-----")
        else:
            Ea = np.abs((Xr - anterior) / Xr) * 100
            print(f"{i+1}\t\t{X1:.6f}\t{X2:.6f}\t{Xr:.6f}\t{f(X1):.6f}\t{f(X2):.6f}\t{f(Xr):.6f}\t{Ea:.6f}%")
            resultado+=f"{i+1}\t\t{X1:.6f}\t{X2:.6f}\t{Xr:.6f}\t{f(X1):.6f}\t{f(X2):.6f}\t{f(Xr):.6f}\t{Ea:.6f}%\n"
    
        anterior=Xr
    
        i +=1

        Fi = f(X1)
        F2 = f(Xr)  # Evaluar en Xr

    # Método de bisección correctamente aplicado
        if Fi * F2 < 0:
            X2 = Xr  # La raíz está en [Xi, Xr]
        else:
            X1 = Xr  # La raíz está en [Xr, X2]


        if Ea <Es:

            break

        Xr = X2 - ((f(X2) * (X1 - X2)) / (f(X1) - f(X2)))
    return resultado
    
    
