from flask import Flask, flash, render_template, make_response, request, redirect, session, url_for, abort, send_file, jsonify
from flask_mysqldb import MySQL
from config import get_connection, DEBUG, PORT
import requests
import logging
from werkzeug.utils import secure_filename
from functools import wraps
import os

app = Flask(__name__)

# Configuración de la clave secreta
app.secret_key = os.urandom(24)

app.config.from_object(get_connection)

# Configurar conexiones a las bases de datos
mysql = MySQL(app)

logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/buscar', methods=['POST'])
def buscar():
    documento = request.form.get('documento')
    fecha_expedicion_ingresada = request.form.get('fecha_expedicion')  # Asumimos que el formulario tiene un campo para la fecha

    #Validar el token con el servidor de Google (COMENTADO)
    recaptcha_response = request.form.get('g-recaptcha-response')
    data = {
         'secret': '6Le464wqAAAAAGuFH7VlDzNyn_F_1i77QXOtMu87',  # Tu clave secreta
         'response': recaptcha_response
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = r.json()
    logging.info("Respuesta de reCAPTCHA: %s", result)
    if result.get('success'):
         flash("Falló la verificación de reCAPTCHA. Inténtalo de nuevo.")
         return redirect(url_for('index'))

    # Validación de entrada
    if not documento or not fecha_expedicion_ingresada:
        flash("Por favor ingrese un número de documento válido y la fecha de expedición.")
        return redirect(url_for('index'))

    try:
        # Conexión a la base de datos `cobros_new`
        conn_cobros = get_connection('db1')
        cursor_cobros = conn_cobros.cursor()
        cursor_cobros.execute(
            "SELECT documento FROM informacion WHERE documento = %s", (documento,)
        )
        resultado_cobros = cursor_cobros.fetchone()
        cursor_cobros.close()
        conn_cobros.close()

        # Conexión a la base de datos `ani` para obtener el ANIFchExpedicion
        conn_ani = get_connection('db2')
        cursor_ani = conn_ani.cursor()
        cursor_ani.execute(
            "SELECT ANINuip, ANIFchExpedicion FROM ani WHERE ANINuip = %s", (documento,)
        )
        resultado_ani = cursor_ani.fetchone()
        cursor_ani.close()
        conn_ani.close()

        # Validar si el documento está en ambas bases de datos
        if resultado_ani and resultado_cobros:
            # Si se encuentra, validar la fecha de expedición
            fecha_expedicion_ani = resultado_ani[1]  # Suponiendo que ANIFchExpedicion es el segundo campo en el resultado
            if fecha_expedicion_ingresada != str(fecha_expedicion_ani):
                flash("La fecha de expedición ingresada no coincide con la cedula ingresada.")
                return redirect(url_for('index'))
            session['documento'] = documento
            return redirect(url_for('consulta'))
        elif resultado_ani:
            flash("El documento no tiene sanciones registradas.")
            return redirect(url_for('index'))
        else:
            flash("No se encontró información para el documento proporcionado.")
            return redirect(url_for('index'))

    except Exception as e:
        flash(f"Error al realizar la consulta: {str(e)}")
        return redirect(url_for('index'))


@app.route('/consulta')
def consulta():
    documento = session.get('documento')
    
    if not documento:
        flash("No hay un documento en la sesión. Realice la búsqueda nuevamente.")
        return redirect(url_for('index'))

    try:
        # Consultar detalles en cobros_new
        connection_cobros = get_connection('db1')  # Conexión a cobros_new
        with connection_cobros.cursor() as cursor_cobros:
            cursor_cobros.execute(
                """
                SELECT i.documento, i.n1, i.n2, i.a1, i.a2, i.valor_sancion, i.coddep, d.nomdep
                FROM informacion i
                LEFT JOIN deptos d ON i.coddep = d.coddep
                WHERE i.documento = %s
                """,
                (documento,)
            )
            detalles = cursor_cobros.fetchall()

        if not detalles:
            flash("No se encontraron resultados adicionales.")
            return redirect(url_for('index'))

        return render_template(
            'consulta.html',
            detalles=detalles,
        )

    except Exception as e:
        flash(f"Ocurrió un error al realizar la consulta: {str(e)}")
        return redirect(url_for('index'))



@app.route('/footer')
def footer():
    return render_template('footer.html')


@app.route('/header')
def header():
    return render_template('header.html')


if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
