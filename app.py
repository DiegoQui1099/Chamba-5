from flask import Flask, flash, render_template, make_response, request, redirect, session, url_for, abort, send_file, jsonify
from flask_mysqldb import MySQL
from config import Config
import requests
import logging
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)
#app.secret_key = Config.SECRET_KEY

# Configurar conexiones a las bases de datos
mysql = MySQL(app)

# Segunda base de datos (ani)
app.config['MYSQL_FECHA_HOST'] = Config.MYSQL_FECHA_HOST
app.config['MYSQL_FECHA_USER'] = Config.MYSQL_FECHA_USER
app.config['MYSQL_FECHA_PASSWORD'] = Config.MYSQL_FECHA_PASSWORD
app.config['MYSQL_FECHA_DB'] = Config.MYSQL_FECHA_DB

mysql_fecha = MySQL(app)

logging.basicConfig(level=logging.INFO)
#SECRET_KEY = '6Le464wqAAAAAGuFH7VlDzNyn_F_1i77QXOtMu87'

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# Ruta que recibe la cédula y redirige a /consulta
@app.route('/buscar', methods=['POST'])
def buscar():
    documento = request.form.get('documento')

    # Validación de entrada
    if not documento:
        flash("Por favor ingrese un número de documento válido.")
        return redirect(url_for('index'))

    # Consulta en la base de datos principal (cobros_new)
    cursor_cobros = mysql.connection.cursor()  # Usa `mysql` para cobros_new
    cursor_cobros.execute(
        "SELECT documento FROM informacion WHERE documento = %s",
        (documento,)
    )
    resultado_cobros = cursor_cobros.fetchone()
    cursor_cobros.close()

    if resultado_cobros:
        # Si el documento existe, verificamos en la base de datos ani
        cursor_ani = mysql_fecha.connection.cursor()  # Usa `mysql_fecha` para ani
        cursor_ani.execute(
            "SELECT ANIFchExpedicion FROM ani WHERE ANINuip = %s",
            (documento,)
        )
        resultado_ani = cursor_ani.fetchone()
        cursor_ani.close()

        if resultado_ani:
            # Guardar el documento y fecha de expedición en la sesión
            session['documento'] = documento
            session['ANIFchExpedicion'] = resultado_ani[0]
            return redirect(url_for('consulta'))
        else:
            flash("No se encontró información de expedición para este documento.")
            return redirect(url_for('index'))
    else:
        flash("No se encontró información para el documento proporcionado.")
        return redirect(url_for('index'))


# Ruta para mostrar los detalles del jurado en consulta.html
@app.route('/consulta')
def consulta():
    documento = session.get('documento')
    fecha_expedicion = session.get('ANIFchExpedicion')

    # Validar si hay datos en la sesión
    if not documento or not fecha_expedicion:
        flash("No se ha realizado ninguna consulta válida.")
        return redirect(url_for('index'))

    try:
        # Consultar detalles en cobros_new
        cursor_cobros = mysql.connection.cursor()  # Usa `mysql` para cobros_new
        cursor_cobros.execute(
            """
            SELECT documento, n1, n2, a1, a2, valor_sancion, coddep 
            FROM informacion 
            WHERE documento = %s
            """,
            (documento,)
        )
        detalles = cursor_cobros.fetchall()
        cursor_cobros.close()

        if not detalles:
            flash("No se encontraron resultados adicionales.")
            return redirect(url_for('index'))

        # Mostrar resultados en consulta.html
        return render_template(
            'consulta.html',
            detalles=detalles,
            fecha_expedicion=fecha_expedicion
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


@app.route('/test_db')
def test_db():
    cursor = mysql.connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    cursor.close()
    return f"Tablas en la base de datos: {tables}"

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])




    # Validar el token con el servidor de Google (COMENTADO)
    # recaptcha_response = request.form.get('g-recaptcha-response')
    # data = {
    #     'secret': '6Le464wqAAAAAGuFH7VlDzNyn_F_1i77QXOtMu87',  # Tu clave secreta
    #     'response': recaptcha_response
    # }
    # r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    # result = r.json()
    # logging.info("Respuesta de reCAPTCHA: %s", result)
    # if not result.get('success'):
    #     flash("Falló la verificación de reCAPTCHA. Inténtalo de nuevo.")
    #     return redirect(url_for('index'))