# modules/query_tools.py
# Herramientas para aprender SQL y consultar la base de datos
import sqlite3

DB_PATH = "data/historial_postventa.db"

def conectar():
    """Abre conexión con la BD."""
    return sqlite3.connect(DB_PATH)

# ==============================================================
# 1. CONSULTAR TODAS LAS FILAS (primer paso básico)
# ==============================================================

def ver_primeras_filas(limit=10):
    """Devuelve las primeras filas de la tabla historial."""
    con = conectar()
    cur = con.cursor()
    cur.execute(f"SELECT * FROM historial LIMIT {limit}")
    filas = cur.fetchall()
    con.close()
    return filas

# ==============================================================
# 2. OBTENER LISTA DE COLUMNAS
# ==============================================================

def obtener_columnas():
    """Muestra todas las columnas de la tabla."""
    con = conectar()
    cur = con.cursor()
    cur.execute("PRAGMA table_info(historial)")
    columnas = cur.fetchall()
    con.close()
    return columnas

# ==============================================================
# 3. CONTAR REGISTROS POR ESTADO
# ==============================================================

def contar_por_estado():
    """Ejemplo: cuántos ticket están en cada estado."""
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        SELECT estado, COUNT(*) 
        FROM historial
        GROUP BY estado
        ORDER BY COUNT(*) DESC
    """)
    datos = cur.fetchall()
    con.close()
    return datos

# ==============================================================
# 4. LISTAR CASAS CON MÁS REPORTES
# ==============================================================

def top_casas(n=10):
    con = conectar()
    cur = con.cursor()
    cur.execute(f"""
        SELECT casa, COUNT(*)
        FROM historial
        GROUP BY casa
        ORDER BY COUNT(*) DESC
        LIMIT {n}
    """)
    datos = cur.fetchall()
    con.close()
    return datos
