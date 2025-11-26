
# Copyright (c) 2025 JOSE ROCHA. Todos los derechos reservados.
import pandas as pd

def leer_excel(ruta_excel: str) -> pd.DataFrame:
    """
    Lee el archivo Excel original sin modificarlo.
    Devuelve un DataFrame crudo para procesar con el ETL.
    """
    try:
        df = pd.read_excel(ruta_excel)
        print("✔ Excel leído correctamente.")
        return df
    except Exception as e:
        print(f"❌ Error al leer el Excel: {e}")
        return None
    