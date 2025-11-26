# 🏗️ Sistema ETL + SQLite + PDF Generator para Informes de Postventa

Automatización completa para procesar informes de postventa que originalmente venían en Excel con cientos de columnas pivotadas.
Este proyecto transforma esos datos en un formato normalizado, los almacena en una base de datos historial y genera un **informe PDF profesional** con métricas clave.



## 🚀 Características principales

* 📥 **Lectura automática del archivo Excel** original (pivotado).
* 🧽 **ETL completo**:

  * Limpieza de encabezados
  * Detección de columnas
  * Normalización (UNPIVOT)
* 🗄️ **Almacenamiento en SQLite** con historial de reportes.
* 📊 **Generación de métricas**:

  * Total por estado
  * Casas con más reportes
  * Capítulos más frecuentes
* 📄 **Generación de PDF** con formato profesional.
* ⚙️ Arquitectura modular (cada parte del sistema está separada por responsabilidad).

---

## 📁 Estructura del proyecto

```
POSTVENTA/
│── main.py
│── input/
│   └── INFORME POSTVENTA BORRADOR.xlsx
│── data/
│   └── historial_postventa.db
│── output/
│   └── informe_postventa.pdf
│── modules/
│   ├── file_reader.py
│   ├── etl.py
│   ├── storage.py
│   ├── metrics.py
│   ├── pdf_generator.py
│   ├── ui_forms.py
│── README.md
```



# 🧪 Instalación y configuración

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/postventa-etl.git
cd postventa-etl
```

### 2️⃣ Crear entorno virtual

```bash
python -m venv .venv
```

### 3️⃣ Activar entorno

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / Mac**

```bash
source .venv/bin/activate
```

### 4️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

*(Si quieres, te genero tu archivo **requirements.txt**)*

### 5️⃣ Colocar el archivo Excel en:

```
/input/INFORME POSTVENTA BORRADOR.xlsx
```

### 6️⃣ Ejecutar el sistema

```bash
python main.py
```

---

# 🔧 Tecnologías utilizadas

| Tecnología               | Uso                               |
| ------------------------ | --------------------------------- |
| **Python 3.10+**         | Lenguaje principal                |
| **Pandas**               | Transformación de datos           |
| **SQLite3**              | Motor de BD ligero para historial |
| **FPDF**                 | Generación del informe en PDF     |
| **OpenPyXL**             | Soporte para lectura de Excel     |
| **Arquitectura Modular** | Separación por responsabilidades  |



# 🔍 Proceso ETL (Explicación)

### ✔ 1. Lectura del archivo Excel

```python
df = pd.read_excel("input/INFORME POSTVENTA BORRADOR.xlsx")
```

### ✔ 2. Limpieza de encabezados

* El archivo original tiene filas vacías.
* Se detecta automáticamente la fila que contiene “DETALLE”.

```python
fila_header = df[df.apply(lambda r: r.astype(str).str.contains("DETALLE").any(), axis=1)].index[0]
```

### ✔ 3. Detección de columnas

* Columnas fijas (área, item, detalle, capítulo)
* Columnas de casas (CASA #02, CASA #03, etc.)

### ✔ 4. Normalización (UNPIVOT / MELT)

```python
df_normalizado = df.melt(
    id_vars=[area, item, detalle, capitulo],
    value_vars=columnas_casas,
    var_name="casa",
    value_name="estado"
)
```

---

# 🗄️ Base de datos

El sistema guarda cada ejecución como un **snapshot histórico**:

```sql
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
```

✔ Permite construir métricas históricas.
✔ Permite generar reportes comparativos en el futuro.



# 📊 Métricas generadas

```python
{
  "total_por_estado": [...],
  "top_5_casas": [...],
  "top_3_capitulos": [...]
}
```

Ejemplo:

* POSTVENTA CORREGIDA → 5606
* TIENE POSTVENTA → 552
* CASA #03 → 175 reportes
* Capítulo "PINTURA" → 892 incidencias



# 📄 PDF generado

El sistema crea automáticamente:

```
/output/informe_postventa.pdf
```

Incluye:

* Título y fecha
* Totales
* Ranking de casas
* Ranking de capítulos
* Lista de estados

Código principal:

```python
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

for estado, total in resumen["total_por_estado"]:
    pdf.cell(0, 8, f"- {estado}: {total}", ln=True)

pdf.output("output/informe_postventa.pdf")
```


# 📌 Próximas mejoras

* UI con Tkinter / PySide6
* Dashboard con Streamlit
* Gráficos en el PDF
* Exportar a Excel normalizado
* API REST con FastAPI



# 👤 Autor

**Jose Rocha**
Desarrollador Python – Enfocado en automatización, ETL & DevOps.


# ⭐ Contribuye

¿Ideas, PRs o mejoras?
¡Bienvenidas!

---

