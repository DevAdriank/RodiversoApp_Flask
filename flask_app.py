# print("Bienvenidos a Python")
from flask import Flask, render_template, request, redirect, session, url_for, jsonify, abort, flash
import pyodbc
from encriptar import User
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, login_manager
import time
import os 

app = Flask(__name__ , template_folder='templates')

app.secret_key = 'rodiverso'  # Esta clave se utiliza para encriptar la sesión del usuario
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    cursor = cnxn.cursor()
    cursor.execute("SELECT usoLogin, usoClave FROM usuario WHERE usoLogin=?", (user_id,))
    row = cursor.fetchone()
    if row is None:
        return None
    else:
        username, password = row
        user = User(username, password)
        return user

AUTHORIZED_MACS = ['74:4C:A1:D0:B5:67', '66:77:88:99:AA:BB']

# Configuración de la base de datos----------------------------------------------------------
SERVER = 'LAPTOP-22JFPE21\\NECAR,49172'
DATABASE = 'Necar_Test'
USER = 'sa'
PASSWORD = '123'
DRIVER = '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect(f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={USER};PWD={PASSWORD}')

#RutaPrincipal para Login----------------------------------------------------------
@app.route("/rodiverso", methods=['GET','POST'])
def home():

        return render_template('index.html')

#Formulario para Loguear----------------------------------------------------------
@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        # Obtener los datos de inicio de sesión del formulario
        username = request.form['username']
        password = request.form['password']

        # Verificar si el usuario y contraseña son válidos en la base de datos
        cursor = cnxn.cursor()
        cursor.execute("SELECT usoLogin, usoClave FROM usuario WHERE usoLogin=? AND usoClave=?", (username, password))
        row = cursor.fetchone()
        if row is None:
            # Si la autenticación falla, muestra un mensaje de error.
            mensaje = "Contraseña Incorrecta"
            flash(mensaje, 'danger')
            return render_template('index.html', error='Usuario o contraseña incorrectos')
        else:
            user = User(username, password)
            login_user(user)

            # Redirige al usuario a la página principal.
            return redirect(url_for('opciones'))
        
#Formulario para Consulta de Clientes----------------------------------------------------------
@app.route("/opciones")
@login_required 
def opciones():
   
    return render_template('opciones.html')

#Agrega el Usuario a la base de Datos
# @app.route('/agregar_cliente', methods=['POST'])
# def agregar_cliente():
#   # Obtener los datos del formulario
#   cursor.execute(f"INSERT INTO cliente (CteCedula, CteNombre, CteUrbanizacion, CteTelefono) VALUES ('{cedula}', '{nombre}', '{urbanizacion}', '{telefono}')")        

#Formulario para Consulta de Clientes------------------------------------------------
@app.route("/consulta")
@login_required 
def consulta():
   
    return render_template('consulta.html')

#Formulario para Registro de Clientes-------------------------------------------------
@app.route("/registro")
@login_required 
def registro():
    
    return render_template('registro.html')
    
#Formulario para Cliente Encontrado----------------------------------------------------
@app.route("/cliente_encontrado")
@login_required 
def cliente_encontrado(cedula):
    
    return render_template('cliente_encontrado.html')

# Ruta para procesar la búsqueda de Cliente por cedula------------------------------------
@app.route('/procesar_busqueda', methods=['GET','POST'])
@login_required
def procesar_busqueda():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'buscar':
            # código para consulta
            cursor = cnxn.cursor()
            cedula = request.form['cedula']
            cursor.execute(f"SELECT * FROM cliente WHERE cteCedula = '{cedula}'")
            cliente = cursor.fetchone()
            print (cedula)
            if cliente:
                # Si el cliente existe, mostrar sus datos
                return render_template('cliente_encontrado.html', cliente=cliente)
            elif cliente is None:
                # Si el cliente no existe, invitar a registrarse
                return redirect(url_for('registro'))
        if action == 'atras':
            return redirect(url_for('opciones'))

    else:
        return render_template('opciones')


# Ruta para procesar Opciones------------------------------------
@app.route('/registro_o_consulta', methods=['POST'])
def registro_o_consulta():
	action = request.form['action']
	if action == 'consulta':
		# código para consulta
		return redirect(url_for('consulta'))
	elif action == 'registro':
		# código para registrarse
		return redirect(url_for('registro'))


#Procesa un NUEVO registro o cliente------------------------------------
@app.route('/procesar_registro', methods=['GET','POST'])
def procesar_registro():

    if request.method == 'POST':
        action = request.form['action']
        if action == 'registrar':
            cursor = cnxn.cursor()
            cedula = request.form.get('cedula')
            nombre = request.form.get('nombre')
            telefono = request.form.get('telefono')
            direccion = request.form.get('direccion')

            # Validar los campos del formulario
            if not cedula or not nombre or not telefono or not direccion:
                mensaje_error = "Todos los campos son requeridos."
                return render_template('cliente_encontrado.html', mensaje_error=mensaje_error)

            if not cedula.isdigit():
                mensaje_error = "La cédula debe ser un número."
                return render_template('cliente_encontrado.html', mensaje_error=mensaje_error)

            if not telefono.isdigit():
                mensaje_error = "El teléfono debe ser un número."
                return render_template('cliente_encontrado.html', mensaje_error=mensaje_error)
            print(cedula, nombre, telefono, direccion)
            cursor.execute("INSERT INTO cliente (cteCedula, cteNombre, cteTelefono, cteUrbanizacion) VALUES (?, ?, ?, ?)", (cedula, nombre, telefono, direccion))
            id_generado = cursor.execute("SELECT SCOPE_IDENTITY()").fetchone()[0]
            print(id_generado)
            
            cursor.execute(f"SELECT * FROM cliente WHERE cteCedula = '{cedula}'")
            cliente = cursor.fetchone()
            cnxn.commit()
            # cnxn.close()
            mensaje = "El cliente se actualizó con éxito"
            flash(mensaje, 'success')
            return render_template('cliente_actualizado.html', cliente=cliente)
        
            # else:
            #     mensaje_error = "No se pudo registrar el cliente"
            #     return render_template('registro.html', mensaje_error=mensaje_error)
        if action == 'atras':
            return redirect(url_for('opciones'))   
    else:
         
        return render_template('opciones', mensaje_exito="Formulario procesado con éxito.")


#Actualiza un registro o cliente------------------------------------------------------
@app.route('/actualiza_registro', methods=['GET','POST'])
def actualiza_registro():

    if request.method == 'POST':
        action = request.form['action']
        if action == 'actualizar':
            cedula = request.form.get('cteCedula')
            nombre = request.form.get('cteNombre')
            telefono = request.form.get('cteTelefono')
            direccion = request.form.get('cteUrbanizacion')

            # Validar los campos del formulario
            if not cedula or not nombre or not telefono or not direccion:
                mensaje_error = "Todos los campos son requeridos."
                return render_template('cliente_encontrado.html', mensaje_error=mensaje_error)

            if not cedula.isdigit():
                mensaje_error = "La cédula debe ser un número."
                return render_template('cliente_encontrado.html', mensaje_error=mensaje_error)

            if not telefono.isdigit():
                mensaje_error = "El teléfono debe ser un número."
                return render_template('cliente_encontrado.html', mensaje_error=mensaje_error)

            cursor = cnxn.cursor()
            cursor.execute("UPDATE cliente SET cteNombre = ?, cteTelefono = ?, cteUrbanizacion = ? WHERE cteCedula = ?", (nombre, telefono, direccion, cedula))
            cnxn.commit()
            if cursor.rowcount == 0:
                # Si la actualización no afectó ningún registro, muestra un mensaje de error.
                mensaje_error="No se pudo actualizar el Cliente"
                return render_template('cliente_encontrado.html', mensaje_error=mensaje_error)
            else:
                # Obtener los datos del cliente actualizados de la base de datos
                cedula = request.form.get('cteCedula')
                print(cedula)
                cursor.execute("SELECT * FROM cliente WHERE cteCedula = ?", (cedula))
                row = cursor.fetchone()
                cliente = {
                    'cteCedula': row[1],
                    'cteNombre': row[2],
                    'cteTelefono': row[4],
                    'cteUrbanizacion': row[3]
                }
                mensaje = "El cliente se actualizó con éxito"
                flash(mensaje, 'success')
                # time.sleep(1)  # Espera 3 segundos antes de redirigir
                return render_template('cliente_actualizado.html', cliente=cliente)
        if action == 'atras':
            return redirect(url_for('consulta'))
        if action == 'home':
            return redirect(url_for('opciones'))
    else:
        return redirect(url_for('buscar_cliente'))
    
    
#Final de Flask---------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 1000, debug=False)
