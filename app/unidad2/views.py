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


@unidad2.route('/falsPosion', methods=['GET'])
def mostrar_FalsaPosicion():
    keyboard_content = render_template('KeyboardMath.html', time=time.time())
    return render_template('unidad2/metodoFalsaPosicion.html', keyboard_content=keyboard_content, time=time.time())

# Devuelve el resultado de Falsa Posicion


@unidad2.route('/falsaP-json', methods=['POST'])
def falsaPosicion_json():
    from .metodoFalsaPosicion import falsaPosicion
    try:
        data = request.get_json()  # Captura el JSON enviado desde el cliente

        ecuacion = data['ecuacion']
        a = float(data['a'])
        b = float(data['b'])
        tol = float(data['tolerancia'])
        print(ecuacion)
        resultado = falsaPosicion(ecuacion, a, b, tol)
        return resultado

    except (ValueError, KeyError):
        return jsonify({'error': 'Datos inválidos o incompletos'}), 400

# MUESTRA EL METODO DE LA PUNTO FIJO


@unidad2.route('/puntoFijo', methods=['GET'])
def mostrar_puntoFijo():
    keyboard_content = render_template('KeyboardMath.html', time=time.time())
    return render_template('unidad2/puntoFijo.html', keyboard_content=keyboard_content, time=time.time())
# Devuelve el resultado de Punto Fijo


@unidad2.route('/puntoFijo-json', methods=['POST'])
def puntoFijo_json():
    from .puntoFijo import puntoFijo
    try:
        data = request.get_json()  # Captura el JSON enviado desde el cliente

        ecuacion = data['ecuacion']
        a = float(data['a'])
        tol = float(data['tolerancia'])
        print(ecuacion)
        resultado = puntoFijo(ecuacion, a, tol)
        return resultado

    except (ValueError, KeyError):
        return jsonify({'error': 'Datos inválidos o incompletos'}), 400
