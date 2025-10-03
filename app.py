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
# FUNCIÓN 2: AGREGAR DATOS (CREATE) - Separada y alineada a la izquierda
# ------------------------------------------------------------------
@app.route('/agregar', methods=['GET', 'POST'])
def agregar_contacto():
    # 4 ESPACIOS ADELANTE
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
            conexion.commit() # ¡Guardar los cambios!
            
            # 12 ESPACIOS ADELANTE
            return redirect(url_for('index'))
            
        except mysql.connector.Error as err:
            # 8 ESPACIOS ADELANTE
            return f"Error al insertar: {err}"
            
        finally:
            # 8 ESPACIOS ADELANTE
            if 'conexion' in locals() and conexion.is_connected():
                # 12 ESPACIOS ADELANTE
                cursor.close()
                conexion.close()
    
    # 4 ESPACIOS ADELANTE
    # Si el método es GET, simplemente muestra el formulario HTML
    return render_template('formulario.html')


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