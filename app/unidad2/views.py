from flask import Flask, request, render_template
from . import unidad2 

@unidad2.route('/unidad2', methods=['GET', 'POST'])
def biseccion():
    print('entro')
    if request.method == 'POST':
        # Obtener datos del formulario
        a = float(request.form['a'])
        b = float(request.form['b'])
        tol = float(request.form['tol'])
        
        # Aquí puedes agregar tu lógica del método de bisección
        resultado = f"Valores recibidos - a: {a}, b: {b}, tolerancia: {tol}"
        
        return resultado  # Devuelve respuesta al cliente
    
    return render_template('unidad2/biseccion.html')  # Renderiza el formulario si es GET
