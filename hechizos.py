import sqlite3
import os
import re

# Crear la tabla 'hechizos'
def crear_tabla_hechizos():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS hechizos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            nivel INTEGER NOT NULL,
            magia TEXT NOT NULL,
            coste TEXT NOT NULL,
            rango INTEGER NOT NULL,
            duracion TEXT NOT NULL,
            casteo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            clase TEXT,
            raza TEXT,
            otro TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Obtener un hechizo por nombre
def get_hechizo(nombre):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM hechizos WHERE nombre = ?', (nombre,))
    fila = cursor.fetchone()

    conn.close()

    if fila:
        return {
            "id": fila[0],
            "nombre": fila[1],
            "nivel": fila[2],
            "magia": fila[3].split(",") if fila[3] else [],  # Convierte en lista separada por comas
            "coste": fila[4],
            "rango": fila[5],
            "duracion": fila[6],
            "casteo": fila[7],
            "descripcion": fila[8],
            "clase": fila[9],
            "raza": fila[10],
            "otro": fila[11]
        }
    return None


# Obtener todos los hechizos
def get_all_hechizos():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, nombre, nivel, magia, coste, rango, duracion, casteo, descripcion, clase, raza, otro FROM hechizos')
    filas = cursor.fetchall()

    conn.close()

    hechizos = [
        {
            "id": fila[0],
            "nombre": fila[1],
            "nivel": fila[2],
            "magia": fila[3].split(",") if fila[3] else [],  # Convierte en lista separada por comas
            "coste": fila[4],
            "rango": fila[5],
            "duracion": fila[6],
            "casteo": fila[7],
            "descripcion": fila[8],
            "clase": fila[9],
            "raza": fila[10],
            "otro": fila[11]
        }
        for fila in filas
    ]
    return hechizos

def get_all_hechizos_por_clase():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, nombre, nivel, magia, coste, rango, duracion, casteo, descripcion, clase, raza, otro FROM hechizos')
    filas = cursor.fetchall()

    conn.close()

    # Diccionario para almacenar hechizos categorizados por clase
    hechizos_por_clase = {
        "Hechicero": [],
        "Clérigo": [],
        "Bardo": [],
        "Monje": [],
        "Paladín": []
    }

    # Rellenar el diccionario con hechizos por clase
    for fila in filas:
        hechizo = {
            "id": fila[0],
            "nombre": fila[1],
            "nivel": fila[2],
            "magia": fila[3].split(",") if fila[3] else [],  # Convierte en lista separada por comas
            "coste": fila[4],
            "rango": fila[5],
            "duracion": fila[6],
            "casteo": fila[7],
            "descripcion": fila[8],
            "clase": fila[9],
            "raza": fila[10],
            "otro": fila[11]
        }

        
        # Agregar el hechizo a la clase correspondiente
        if fila[9] in hechizos_por_clase:
            hechizos_por_clase[fila[9]].append(hechizo)

    return hechizos_por_clase

# Agregar un hechizo
def agregar_hechizo(nombre, nivel, magia, coste, rango, duracion, casteo, descripcion, clase="", raza="", otro=""):
    if not re.match(r"^\d+(,\d+)*$", coste.strip()):
        print("El formato del coste no es válido. Debe ser del tipo S,M,R con S = Salud, M = Mana, R = Resistencia.")
        return

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(''' 
            INSERT INTO hechizos (nombre, nivel, magia, coste, rango, duracion, casteo, descripcion, clase, raza, otro) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, nivel, magia, coste, rango, duracion, casteo, descripcion, clase, raza, otro))

        conn.commit()
        print("Hechizo agregado con éxito.")
    except sqlite3.Error as e:
        print(f"Error al agregar el hechizo a la base de datos: {e}")
    finally:
        conn.close()


# Borrar un hechizo por nombre
def borrar_hechizo(nombre):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM hechizos WHERE nombre = ?', (nombre,))
        conn.commit()
        print("Hechizo borrado con éxito.")
    except sqlite3.Error as e:
        print(f"Error al borrar el hechizo: {e}")
    finally:
        conn.close()
        
        
import sqlite3

def get_hechizos_magia(magia):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Usamos LIKE para buscar dentro de la lista separada por comas
        cursor.execute("SELECT * FROM hechizos WHERE magia LIKE ? or magia = 'No'", ('%' + magia + '%',))
        filas = cursor.fetchall()

        if not filas:
            return None  # Retorna None si no hay resultados

        hechizos = [
            {
                "id": fila[0],
                "nombre": fila[1],
                "nivel": fila[2],
                "magia": fila[3].split(",") if fila[3] else [],  # Convierte la cadena en lista
                "coste": fila[4],
                "rango": fila[5],
                "duracion": fila[6],
                "casteo": fila[7],
                "descripcion": fila[8],
                "clase": fila[9],
                "raza": fila[10],
                "otro": fila[11]
            }
            for fila in filas
        ]

        return hechizos

    except sqlite3.Error as e:
        print(f"Error en la base de datos: {e}")
        return None  # Retorna None si hay un error

    finally:
        conn.close()
        
def modificar_hechizo(nombre_hechizo, nombre, nivel, magia, coste, rango, duracion, casteo, descripcion, clase="", raza="", otro=""):
    if not re.match(r"^\d+(,\d+)*$", coste.strip()):
        print("El formato del coste no es válido. Debe ser del tipo S,M,R con S = Salud, M = Mana, R = Resistencia.")
        return

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE hechizos
            SET nombre = ?, nivel = ?, magia = ?, coste = ?, rango = ?, duracion = ?, casteo = ?, descripcion = ?, clase = ?, raza = ?, otro = ?
            WHERE nombre = ?
        ''', (nombre, nivel, magia, coste, rango, duracion, casteo, descripcion, clase, raza, otro, nombre_hechizo))

        conn.commit()
        print("Hechizo actualizado con éxito.")
    except sqlite3.Error as e:
        print(f"Error al actualizar el hechizo en la base de datos: {e}")
    finally:
        conn.close()