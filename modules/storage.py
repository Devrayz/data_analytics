# Copyright (c) 2025 JOSE ROCHA. Todos los derechos reservados.
import sqlite3
from pathlib import Path

# Ruta base de la BD
DB_PATH = Path("data/historial_postventa.db")

# ---------------------------------------------------------
# CONEXIÓN A LA BD
# ---------------------------------------------------------
def get_connection():
    """
    Crea o abre la base de datos SQLite.
    Devuelve una conexión lista para usar.
    """
    # Asegurar que la carpeta data exista
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    return conn


# ---------------------------------------------------------
# CREACIÓN DE TABLA
# ---------------------------------------------------------
def crear_tabla_historial():
    """
    Crea la tabla principal si no existe.
    Tabla normalizada:
        area, item, detalle, capitulo, casa, estado, fecha_reporte
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area TEXT,
            item TEXT,
            detalle TEXT,
            capitulo TEXT,
            casa TEXT,
            estado TEXT,
            fecha_reporte TEXT
        );
    """)

    conn.commit()
    conn.close()

    print("✔ Tabla 'historial' lista.")


# ---------------------------------------------------------
# GUARDAR ARCHIVO NORMALIZADO
# ---------------------------------------------------------
def guardar_historial(df, fecha_reporte: str):
    """
    Guarda los datos del DataFrame normalizado en SQLite.
    """
    crear_tabla_historial()

    conn = get_connection()
    cursor = conn.cursor()

    registros = df.to_dict(orient="records")

    for record in registros:
        cursor.execute("""
            INSERT INTO historial (area, item, detalle, capitulo, casa, estado, fecha_reporte)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            record.get("area"),
            record.get("item"),
            record.get("detalle"),
            record.get("capitulo"),
            record.get("casa"),
            record.get("estado"),
            fecha_reporte
        ))

    conn.commit()
    conn.close()

    print(f"✔ {len(registros)} registros guardados en la base de datos.")
