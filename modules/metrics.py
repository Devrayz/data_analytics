# modules/metrics.py
# Copyright (c) 2025 JOSE ROCHA. Todos los derechos reservados.
"""
Consultas/metrìcas sobre la tabla historial en SQLite.

Funciones:
- total_por_estado(conn)
- top_n_casas_mas_fallos(conn, n=5)
- top_n_capitulos(conn, n=3)
- conteo_por_area(conn)
- resumen_metricas(conn)  -> devuelve un dict con todas las métricas principales
"""

import sqlite3
from typing import List, Tuple, Dict

# IMPORTA get_connection desde donde lo dejaste
# Si tu get_connection está en storage.py a nivel raíz, ajusta la importación:
from modules.storage import get_connection


def total_por_estado(conn: sqlite3.Connection) -> List[Tuple[str, int]]:
    """
    Retorna lista de tuplas (estado, total)
    """
    cur = conn.cursor()
    cur.execute("""
        SELECT estado, COUNT(*) as total
        FROM historial
        GROUP BY estado
        ORDER BY total DESC;
    """)
    return cur.fetchall()


def top_n_casas_mas_fallos(conn: sqlite3.Connection, n: int = 5) -> List[Tuple[str, int]]:
    """
    Retorna top N casas con más registros (fallos/postventas).
    Devuelve lista de (casa, total).
    """
    cur = conn.cursor()
    cur.execute("""
        SELECT casa, COUNT(*) as total
        FROM historial
        GROUP BY casa
        ORDER BY total DESC
        LIMIT ?;
    """, (n,))
    return cur.fetchall()


def top_n_capitulos(conn: sqlite3.Connection, n: int = 3) -> List[Tuple[str, int]]:
    """
    Top N capítulos con más incidencias.
    """
    cur = conn.cursor()
    cur.execute("""
        SELECT capitulo, COUNT(*) as total
        FROM historial
        GROUP BY capitulo
        ORDER BY total DESC
        LIMIT ?;
    """, (n,))
    return cur.fetchall()


def conteo_por_area(conn: sqlite3.Connection) -> List[Tuple[str, int]]:
    """
    Conteo de incidencias por área.
    """
    cur = conn.cursor()
    cur.execute("""
        SELECT area, COUNT(*) as total
        FROM historial
        GROUP BY area
        ORDER BY total DESC;
    """)
    return cur.fetchall()


def resumen_metricas(conn: sqlite3.Connection) -> Dict[str, object]:
    """
    Ejecuta las métricas principales y devuelve un diccionario con resultados.
    Útil para pasar luego al generador de PDF.
    """
    resumen = {
        "total_por_estado": total_por_estado(conn),
        "top_5_casas": top_n_casas_mas_fallos(conn, 5),
        "top_3_capitulos": top_n_capitulos(conn, 3),
        "conteo_por_area": conteo_por_area(conn)
    }
    return resumen


# Modo de prueba / ejemplo de uso
if __name__ == "__main__":
    conn = get_connection()
    r = resumen_metricas(conn)
    print("Total por estado:", r["total_por_estado"])
    print("Top 5 casas:", r["top_5_casas"])
    print("Top 3 capítulos:", r["top_3_capitulos"])
    print("Conteo por área (top):", r["conteo_por_area"][:10])
    conn.close()
