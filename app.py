from dotenv import load_dotenv
import os
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for # ¡NUEVOS MÓDULOS AQUÍ!
import mysql.connector
# --- CONFIGURACIÓN DE CONEXIÓN (Todo alineado a la izquierda) ---
DB_HOST = "localhost" 
DB_USER = "root"
DB_PASS = os.getenv("DB_PASS") # ¡La contraseña se lee de .env!
DB_NAME = "proyecto_python"

app = Flask(__name__) # Inicializa tu aplicación Flask (el servidor)

# ------------------------------------------------------------------
# FUNCIÓN 1: OBTENER DATOS (READ) - Debe tener su cuerpo completo debajo
# ------------------------------------------------------------------
def obtener_contactos():
    """Función para conectarse a MySQL y obtener todos los contactos."""
    # 4 ESPACIOS ADELANTE
    try:
        conexion = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        cursor = conexion.cursor()
        
        # 8 ESPACIOS ADELANTE
        cursor.execute("SELECT id, nombre, telefono FROM contactos")
        
        resultados = cursor.fetchall()
        return resultados # Devuelve la lista de contactos
        
    except mysql.connector.Error as err:
        # 4 ESPACIOS ADELANTE
        print(f"Error al obtener contactos: {err}")
        return []
        
    finally:
        # 4 ESPACIOS ADELANTE
        if 'conexion' in locals() and conexion.is_connected():
            # 8 ESPACIOS ADELANTE
            cursor.close()
            conexion.close()

# ------------------------------------------------------------------
# FUNCIÓN 2: AGREGAR DATOS (CREATE)
# ------------------------------------------------------------------
@app.route('/agregar', methods=['GET', 'POST'])
def agregar_contacto():
    # 4 ESPACIOS ADELANTE (Empieza el bloque IF)
    if request.method == 'POST':
        # 8 ESPACIOS ADELANTE
        nombre_nuevo = request.form['nombre']
        telefono_nuevo = request.form['telefono']
        
        try:
            # 8 ESPACIOS ADELANTE
            conexion = mysql.connector.connect(
                host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
            )
            cursor = conexion.cursor()
            
            consulta_sql = "INSERT INTO contactos (nombre, telefono) VALUES (%s, %s)"
            valores = (nombre_nuevo, telefono_nuevo)
            
            cursor.execute(consulta_sql, valores)
            conexion.commit()
            
            # 12 ESPACIOS ADELANTE (PRIMER RETURN)
            return redirect(url_for('index')) # <--- ¡PRIMER RETURN! Redirige después de guardar
            
        except mysql.connector.Error as err:
            # 8 ESPACIOS ADELANTE
            return f"Error al insertar: {err}" # <--- ¡SEGUNDO RETURN! Si hay error de MySQL
            
        finally:
            # 8 ESPACIOS ADELANTE
            if 'conexion' in locals() and conexion.is_connected():
                # 12 ESPACIOS ADELANTE
                cursor.close()
                conexion.close()
    
    # 4 ESPACIOS ADELANTE (Esta línea DEBE estar alineada con el 'if')
    return render_template('formulario.html') # <--- ¡TERCER RETURN! Si solo se pide la página (GET)

# NUEVA FUNCIÓN: ELIMINAR CONTACTO (DELETE)
@app.route('/eliminar/<int:id_contacto>', methods=['POST', 'GET'])
def eliminar_contacto(id_contacto):
    try:
        conexion = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
        )
        cursor = conexion.cursor()
        
        # Comando SQL para eliminar
        consulta_sql = "DELETE FROM contactos WHERE id = %s"
        
        # Ejecutamos el DELETE con el ID que viene de la URL
        cursor.execute(consulta_sql, (id_contacto,))
        conexion.commit() 
        
        # Redirigimos al inicio para ver la lista actualizada
        return redirect(url_for('index'))
        
    except mysql.connector.Error as err:
        return f"Error al eliminar: {err}"
        
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

# ------------------------------------------------------------------
# FUNCIÓN 4: EDITAR DATOS (UPDATE)
# ------------------------------------------------------------------
@app.route('/editar/<int:id_contacto>', methods=['GET', 'POST'])
def editar_contacto(id_contacto):
    # CASO 1: EL USUARIO ENVÍA EL FORMULARIO CON DATOS NUEVOS (POST)
    if request.method == 'POST':
        nombre_editado = request.form['nombre']
        telefono_editado = request.form['telefono']
        
        try:
            conexion = mysql.connector.connect(
                host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
            )
            cursor = conexion.cursor()
            
            # Comando SQL para ACTUALIZAR
            consulta_sql = "UPDATE contactos SET nombre = %s, telefono = %s WHERE id = %s"
            valores = (nombre_editado, telefono_editado, id_contacto)
            
            cursor.execute(consulta_sql, valores)
            conexion.commit()
            
            return redirect(url_for('index'))
            
        except mysql.connector.Error as err:
            return f"Error al actualizar: {err}"
            
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

    # CASO 2: EL USUARIO SOLO PIDE EL FORMULARIO (GET)
    else: 
        try:
            conexion = mysql.connector.connect(
                host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
            )
            cursor = conexion.cursor()
            
            # Comando SQL para SELECCIONAR el contacto actual por ID
            cursor.execute("SELECT id, nombre, telefono FROM contactos WHERE id = %s", (id_contacto,))
            contacto_actual = cursor.fetchone() # Usamos fetchone() porque solo es un registro
            
            if contacto_actual is None:
                return "Contacto no encontrado", 404
            
            # Renderiza el formulario, pero le pasa los datos del contacto
            return render_template('formulario.html', contacto=contacto_actual)
            
        except mysql.connector.Error as err:
            return f"Error al cargar datos de edición: {err}"
            
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

# ------------------------------------------------------------------
# FUNCIÓN 3: RUTA PRINCIPAL (INDEX) - Separada y alineada a la izquierda
# ------------------------------------------------------------------
@app.route('/')
def index():
    # 4 ESPACIOS ADELANTE
    lista_contactos = obtener_contactos() 
    return render_template('contactos.html', contactos=lista_contactos)

if __name__ == '__main__':
    # Inicia el servidor en modo de desarrollo
    app.run(debug=True)