import mysql.connector

# --- 1. CONFIGURACIÓN DE LA CONEXIÓN ---
DB_HOST = "localhost" 
DB_USER = "root"
DB_PASS = "751248963.2025" # ¡IMPORTANTE! Reemplaza aquí
DB_NAME = "proyecto_python"

try:
    # Establecer la conexión
    conexion = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )
    
    if conexion.is_connected():
        print("✅ Conexión exitosa. Leyendo datos...")
        
        cursor = conexion.cursor()
        
        # 2. La consulta SQL para seleccionar todos los registros
        consulta_sql = "SELECT id, nombre, telefono FROM contactos"
        
        # 3. Ejecutar la consulta
        cursor.execute(consulta_sql)
        
        # 4. Obtener todos los resultados (los datos)
        resultados = cursor.fetchall()
        
        print("\n--- REGISTROS EN LA TABLA CONTACTOS ---")
        
        # 5. Iterar sobre los resultados e imprimirlos
        for fila in resultados:
            # fila[0] es el ID, fila[1] es el nombre, fila[2] es el teléfono
            print(f"ID: {fila[0]} | Nombre: {fila[1]} | Teléfono: {fila[2]}")
        
        print("--------------------------------------")


except mysql.connector.Error as err:
    print(f"❌ Error al intentar conectar o leer datos: {err}")

finally:
    # Cerrar la conexión
    if 'conexion' in locals() and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión a MySQL cerrada.")