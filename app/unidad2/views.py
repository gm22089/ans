from flask import Blueprint, request, render_template, jsonify
from . import unidad2
import time

# Muestra el inicio


# MUESTRA EL METODO DE BISECCION

@unidad2.route('/biseccion', methods=['GET'])
def mostrar_biseccion():
    keyboard_content = render_template('KeyboardMath.html', time=time.time())
    return render_template('unidad2/biseccion.html', keyboard_content=keyboard_content, time=time.time())
# Devuelve datos del metodo de biseccion


@unidad2.route('/biseccion-json', methods=['POST'])
def biseccion_json():
    from .biseccion import biseccion
    try:
        data = request.get_json()  # Captura el JSON enviado desde el cliente

        ecuacion = data['ecuacion']
        a = float(data['a'])
        b = float(data['b'])
        tol = float(data['tolerancia'])
        print(ecuacion)
        resultado = biseccion(ecuacion, a, b, tol)
        return resultado

    except (ValueError, KeyError):
        return jsonify({'error': 'Datos inválidos o incompletos'}), 400

    # Renderiza el formulario si es GET
    # return render_template('unidad2/biseccion.html')

# MUESTRA EL METODO DE LA FALSA POSICION


@unidad2.route('/metodoFalsaPosicion', methods=['GET', 'POST'])
def m_falsaPosicion():
    from .metodoFalsaPosicion import falsaPosicion
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            ecuacion = request.form['ecuacionFP']
            a = float(request.form['aFP'])
            b = float(request.form['bFP'])
            tol = float(request.form['toleranciaFP'])
            resultado = falsaPosicion(ecuacion, a, b, tol)
            # Devuelve respuesta al cliente
            return render_template('unidad2/metodoFalsaPosicion.html', resultado=resultado)
        except ValueError:
            return ("Error en los valores ingresados")

    return render_template('unidad2/metodoFalsaPosicion.html')
