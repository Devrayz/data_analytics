from modules.query_tools import (
    ver_primeras_filas,
    obtener_columnas,
    contar_por_estado,
    top_casas
)

print("Primeras filas:")
print(ver_primeras_filas())

print("\nColumnas:")
print(obtener_columnas())

print("\nConteo por estado:")
print(contar_por_estado())

print("\nTop casas:")
print(top_casas(5))
