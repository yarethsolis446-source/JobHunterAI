from services.job_pipeline import JobPipeline
from services.pdf_service import PDFService

from job_sources.aggregator import JobAggregator
from job_sources.test_data_sources import TestDataSource
from job_sources.jsearch_source import JSearchSource

from models.search_request import SearchRequest

import os
from dotenv import load_dotenv



# ==========================
# CARGAR VARIABLES
# ==========================

load_dotenv()


API_KEY = os.getenv(
    "RAPIDAPI_KEY"
)



# ==========================
# CV DE PRUEBA
# ==========================

cv = """

Juan Perez

Software Developer Junior

Experiencia creando aplicaciones
con Python, Java y SQL.

Conocimientos:

Python
Java
SQL
Git
Flutter
JavaScript

Idiomas:

Inglés

Habilidades:

Comunicación
Trabajo en equipo
Resolución de problemas


"""



print("==========================")
print(" INICIANDO JOBHUNTER AI ")
print("==========================")



# ==========================
# CREAR AGREGADOR
# ==========================

aggregator = JobAggregator()



# Fuente de prueba

aggregator.agregar_fuente(

    TestDataSource()

)



# Fuente real

if API_KEY:


    aggregator.agregar_fuente(

        JSearchSource(

            API_KEY

        )

    )



# ==========================
# CREAR PIPELINE
# ==========================

pipeline = JobPipeline(

    aggregator

)



# ==========================
# CONFIGURAR BÚSQUEDA
# ==========================

busqueda = SearchRequest(

    puesto="software developer",

    fecha="week",

    pais="us",

    remoto=False

)



# ==========================
# EJECUTAR
# ==========================

resultado = pipeline.ejecutar(

    cv,

    busqueda

)



# ==========================
# PERFIL
# ==========================

print("\n==========================")
print(" PERFIL ANALIZADO ")
print("==========================")


print(

    resultado["perfil"]

)



# ==========================
# SCORE CV
# ==========================

print("\n==========================")
print(" CALIDAD DEL CV ")
print("==========================")


print(

    "Puntaje:",

    resultado["cv_score"]["score"]

)



print("\nRecomendaciones:")



for r in resultado["cv_score"]["recomendaciones"]:


    print(

        "-",

        r

    )



# ==========================
# EMPLEOS
# ==========================

print("\n==========================")
print(" MEJORES EMPLEOS ")
print("==========================")


if not resultado["empleos"]:


    print(

        "No hay empleos"

    )


else:


    for empleo in resultado["empleos"]:


        print("--------------------------")


        print(

            "Título:",

            empleo.titulo

        )


        print(

            "Empresa:",

            empleo.empresa

        )


        print(

            "Compatibilidad:",

            empleo.score,

            "%"

        )


        print(

            "Nivel:",

            empleo.nivel

        )


        print(

            "Recomendación:",

            empleo.recomendacion

        )


        print(

            "Coincidencias:",

            empleo.coincidencias

        )


        print(

            "Faltantes:",

            empleo.faltantes

        )


        print(

            "Link:",

            empleo.link

        )




# ==========================
# GENERAR PDF
# ==========================

print("\n==========================")
print(" GENERANDO PDF ")
print("==========================")


pdf = PDFService()



archivo = pdf.generar_reporte(

    resultado,

    "JobHunterAI_reporte.pdf"

)



print(

    "PDF creado:",

    archivo

)



print("\n==========================")
print(" PROCESO FINALIZADO ")
print("==========================")