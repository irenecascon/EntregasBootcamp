# Team Challenge SQL – Parte 2: Modelo BigQuery

## Descripción

Este proyecto implementa una base de datos relacional para un e-commerce de productos tecnológicos que opera en varios países de Europa.

El modelo ha sido diseñado hasta la **Tercera Forma Normal (3NF)** e implementado en **Google BigQuery**. Los datos sintéticos se generan con Python mediante la librería **Faker** y posteriormente se cargan en BigQuery para realizar consultas analíticas.

## Tecnologías utilizadas

- Python
- Google BigQuery
- Pandas
- Faker
- Jupyter Notebook
- Google Cloud Service Account

## Estructura del proyecto

```text
parte_2_modelo_bigquery/
├── data/
├── docs/
│   ├── er_diagram.png
│   └── normalizacion.md
└── notebooks/
    ├── 01_setup_bigquery.ipynb
    ├── 02_generate_data.ipynb
    └── 03_queries_verification.ipynb
```

## Modelo de datos

El modelo está compuesto por siete entidades:

- Customers
- Categories
- Products
- Orders
- Order Items
- Payments
- Reviews

La relación muchos a muchos entre **Orders** y **Products** se resuelve mediante la tabla **Order Items**, donde además se almacena el precio histórico, la cantidad y el descuento aplicado.

## Volumen de datos generado

| Tabla | Registros |
|--------|----------:|
| Customers | 500 |
| Categories | 10 |
| Products | 70 |
| Orders | 2.000 |
| Order Items | 4.500 |
| Payments | 2.000 |
| Reviews | 317 |

## Configuración

### Crear el entorno virtual

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

## Configuración de BigQuery

Crear un archivo `.env` con:

```env
GCP_PROJECT_ID=tu-proyecto
BQ_DATASET_ID=tu_dataset
GOOGLE_APPLICATION_CREDENTIALS=./credentials/service-account.json
```

El archivo `.env` y la carpeta `credentials/` no deben subirse al repositorio.

## Ejecución

Los notebooks deben ejecutarse en este orden:

1. `01_setup_bigquery.ipynb`
2. `02_generate_data.ipynb`
3. `03_queries_verification.ipynb`

## Consultas implementadas

Entre las consultas realizadas se incluyen:

- Ventas por categoría.
- Productos más vendidos.
- Clientes con mayor gasto.
- Evolución mensual de ventas.
- Valoración media de productos.
- Resumen de pagos por método y estado.
- Tiempo medio de entrega.