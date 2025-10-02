from flask import Flask, render_template
import mysql.connector

# --- CONFIGURACIÓN DE CONEXIÓN ---
DB_HOST = "localhost" 
DB_USER = "root"
DB_PASS = "751248963.2025" # ¡IMPORTANTE! Reemplaza aquí
DB_NAME = "proyecto_python"

app = Flask(__name__) # Inicializa tu aplicación Flask (el servidor)

def obtener_contactos():
    """Función para conectarse a MySQL y obtener todos los contactos."""
    try:
        conexion = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        cursor = conexion.cursor()
        
        # SQL: Selecciona ID, Nombre y Teléfono (el comando SELECT)
        cursor.execute("SELECT id, nombre, telefono FROM contactos")
        
        # Trae todos los resultados (fetchall)
        resultados = cursor.fetchall()
        
        return resultados # Devuelve la lista de contactos
        
    except mysql.connector.Error as err:
        print(f"Error al obtener contactos: {err}")
        return [] # Devuelve una lista vacía si hay error
        
    finally:
        # Asegura que la conexión se cierre
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

# --- RUTAS WEB ---
# La ruta '/' significa la página principal (ej: http://127.0.0.1:5000/)
@app.route('/')
def index():
    # 1. Obtiene los datos de la base de datos
    lista_contactos = obtener_contactos() 
    
    # 2. Renderiza la plantilla 'contactos.html' y le pasa los datos.
    #    Flask sabe buscar 'contactos.html' dentro de la carpeta 'templates'.
    return render_template('contactos.html', contactos=lista_contactos)

if __name__ == '__main__':
    # Inicia el servidor en modo de desarrollo
    # El puerto por defecto es 5000
    app.run(debug=True)