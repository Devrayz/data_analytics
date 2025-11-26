
# Copyright (c) 2025 JOSE ROCHA. Todos los derechos reservados.
from modules.file_reader import leer_excel
from datetime import datetime
from modules.etl import (
    limpiar_encabezados,
    detectar_columnas_casas,
    detectar_columnas_fijas,
    normalizar_postventas
)
from modules.metrics import resumen_metricas
from modules.storage import get_connection, guardar_historial
from modules.pdf_generator import generar_pdf

RUTA_EXCEL = "input/INFORME POSTVENTA BORRADOR.xlsx"

def main():
    # 1. Leer Excel
    df_raw = leer_excel(RUTA_EXCEL)
    if df_raw is None:
        return

    # 2. Limpiar encabezados
    df_clean = limpiar_encabezados(df_raw)

    # 3. Detectar columnas
    columnas_casas = detectar_columnas_casas(df_clean)
    columnas_fijas = detectar_columnas_fijas(df_clean)

    # 4. Normalizar
    df_normalizado = normalizar_postventas(df_clean, columnas_fijas, columnas_casas)
    print("✔ Data normalizada correctamente.")

    # 5. Guardar en BD
    fecha_reporte = datetime.now().strftime("%Y-%m-%d")
    guardar_historial(df_normalizado, fecha_reporte)

    # 6. Métricas
    resumen = resumen_metricas(conn=get_connection())
    print("✔ Resumen generado:", resumen)

    # 7. Generar PDF
    generar_pdf(resumen)

    print("✔ Proceso completo terminado.")

if __name__ == "__main__":
    main()
