import datetime
import os
import hashlib
from flask import Flask, flash, render_template, make_response, request, redirect, session, url_for, abort, send_file, jsonify
from flask_mysqldb import MySQL
from config import Config
import io
import math
from werkzeug.utils import secure_filename
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = '1234512345'
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# Ruta que recibe la cédula y redirige a /consulta
@app.route('/buscar', methods=['POST'])
def buscar():
    cedula = request.form['cedula']

    # Verifica si la cédula existe en la base de datos
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM multas_jurados WHERE Cedula = %s", (cedula,))
    jurado = cursor.fetchone()
    cursor.close()

    # Si la cédula existe, guarda en la sesión y redirige a /consulta
    if jurado:
        session['cedula'] = cedula  # Guardamos la cédula en la sesión
        return redirect(url_for('consulta'))
    else:
        flash("Cédula no encontrada. Intente nuevamente.")
        return redirect(url_for('index'))

# Ruta para mostrar los detalles del jurado en consulta.html
@app.route('/consulta')
def consulta():
    cedula = session.get('cedula')  # Obtenemos la cédula desde la sesión

    if not cedula:
        flash("No se ha realizado ninguna consulta.")
        return redirect(url_for('index'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT Nombres, Apellidos, Cedula, FechaExp, Departamento, Multa_p, Motivo, observaciones, Id_Jurado FROM multas_jurados WHERE Cedula = %s", (cedula,))
    jurados = cursor.fetchall()
    cursor.close()

    # Si `jurado` tiene datos, estos se pasarán como tupla a `consulta.html`
    return render_template('consulta.html', jurados=jurados)

@app.route('/footer')
def footer():
    return render_template('footer.html')

@app.route('/header')
def header():
    return render_template('header.html')

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])
