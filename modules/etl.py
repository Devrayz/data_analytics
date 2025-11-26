
# Copyright (c) 2025 JOSE ROCHA. Todos los derechos reservados.
import pandas as pd


# ---------------------------------------------------------
# LIMPIEZA DE ENCABEZADOS
# ---------------------------------------------------------
def limpiar_encabezados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia los encabezados del Excel.
    Detecta la fila donde aparece 'DETALLE' y la usa como encabezado real.
    """
    fila_header = df[df.apply(lambda r: r.astype(str).str.contains("DETALLE", case=False).any(), axis=1)].index[0]

    df.columns = df.iloc[fila_header]
    df = df[fila_header + 1:]
    df = df.reset_index(drop=True)

    print("✔ Encabezados limpiados.")
    return df


# ---------------------------------------------------------
# DETECCIÓN DE COLUMNAS
# ---------------------------------------------------------
def detectar_columnas_casas(df: pd.DataFrame) -> list:
    """Detecta columnas que representan casas."""
    columnas_casas = [c for c in df.columns if "CASA" in str(c).upper()]
    print(f"✔ Columnas de casas detectadas: {len(columnas_casas)} columnas.")
    return columnas_casas


def detectar_columnas_fijas(df: pd.DataFrame) -> dict:
    """Detecta columnas base de área, ítem, detalle y capítulo."""
    mapping = {
        "area": None,
        "item": None,
        "detalle": None,
        "capitulo": None
    }

    for col in df.columns:
        col_upper = str(col).upper()

        if "DETALLE" in col_upper:
            mapping["detalle"] = col
        elif "ITEM" in col_upper:
            mapping["item"] = col
        elif "CAPITULO" in col_upper:
            mapping["capitulo"] = col
        elif mapping["area"] is None and "CASA" not in col_upper and "UNNAMED" not in col_upper:
            mapping["area"] = col

    print("✔ Columnas fijas detectadas:", mapping)
    return mapping


# ---------------------------------------------------------
# NORMALIZACIÓN DE DATOS (UNPIVOT)
# ---------------------------------------------------------
def normalizar_postventas(df: pd.DataFrame, mapping: dict, columnas_casas: list) -> pd.DataFrame:
    """
    Convierte el archivo pivotado en una tabla normalizada:
    area, item, detalle, capitulo, casa, estado
    """

    df_normal = df.melt(
        id_vars=[mapping["area"], mapping["item"], mapping["detalle"], mapping["capitulo"]],
        value_vars=columnas_casas,
        var_name="casa",
        value_name="estado"
    )

    # Eliminar filas sin estado
    df_normal = df_normal.dropna(subset=["estado"])

    # Limpiar espacios
    for col in df_normal.columns:
        df_normal[col] = df_normal[col].astype(str).str.strip()

    print("✔ Data normalizada correctamente.")
    return df_normal


# ---------------------------------------------------------
# FUNCIÓN PRINCIPAL ETL
# ---------------------------------------------------------
def procesar_excel(ruta_excel: str) -> pd.DataFrame:
    """
    Flujo ETL completo para convertir el Excel pivotado en tabla normalizada.
    """
    print("🔄 Leyendo archivo Excel...")
    df = pd.read_excel(ruta_excel)

    df = limpiar_encabezados(df)
    mapping = detectar_columnas_fijas(df)
    columnas_casas = detectar_columnas_casas(df)

    df_normal = normalizar_postventas(df, mapping, columnas_casas)
    return df_normal


# ---------------------------------------------------------
# PRUEBA MANUAL
# ---------------------------------------------------------
if __name__ == "__main__":
    ruta = "INFORME POSTVENTA 20251117.xlsx"
    df = procesar_excel(ruta)
    print(df.head())
    print("Total filas:", len(df))
