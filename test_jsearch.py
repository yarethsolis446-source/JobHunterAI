import os
import requests

from pathlib import Path
from dotenv import load_dotenv


# =========================================================
# CONFIGURACIÓN
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)


# =========================================================
# API KEY
# =========================================================

API_KEY = os.getenv(
    "JSEARCH_API_KEY"
)


print()
print("========================================")
print("PRUEBA DIRECTA DE JSEARCH")
print("========================================")


print()
print("Archivo .env:")
print(
    ENV_PATH
)


# =========================================================
# VERIFICAR API KEY
# =========================================================

if not API_KEY:

    print()
    print("❌ ERROR")
    print("No se encontró JSEARCH_API_KEY")
    print()
    print("Revisa que tu .env tenga:")
    print()
    print("JSEARCH_API_KEY=TU_API_KEY")
    print()

    raise SystemExit(1)


# =========================================================
# MOSTRAR KEY PARCIAL
# =========================================================
#
# NO mostramos la API key completa.
#

if len(API_KEY) >= 10:

    key_visible = (
        API_KEY[:6]
        + "..."
        + API_KEY[-4:]
    )

else:

    key_visible = "***"


print()
print("API KEY ENCONTRADA:")
print(
    key_visible
)


# =========================================================
# URL
# =========================================================

URL = (
    "https://jsearch.p.rapidapi.com/search"
)


print()
print("URL:")
print(
    URL
)


# =========================================================
# HEADERS
# =========================================================

headers = {

    "x-rapidapi-host":
        "jsearch.p.rapidapi.com",

    "x-rapidapi-key":
        API_KEY

}


# =========================================================
# PARAMETROS
# =========================================================

params = {

    "query":
        "software developer",

    "page":
        "1",

    "num_pages":
        "1",

    "date_posted":
        "all"

}


print()
print("========================================")
print("PARAMETROS")
print("========================================")


print(
    params
)


# =========================================================
# REQUEST
# =========================================================

print()
print("========================================")
print("ENVIANDO REQUEST...")
print("========================================")


try:

    respuesta = requests.get(

        URL,

        headers=headers,

        params=params,

        timeout=30

    )


except requests.exceptions.Timeout:

    print()
    print("❌ TIMEOUT")
    print(
        "JSearch tardó demasiado en responder."
    )

    raise SystemExit(1)


except requests.exceptions.RequestException as error:

    print()
    print("❌ ERROR DE CONEXIÓN")
    print(
        error
    )

    raise SystemExit(1)


# =========================================================
# STATUS
# =========================================================

print()
print("========================================")
print("RESPUESTA")
print("========================================")


print()
print(
    "STATUS:",
    respuesta.status_code
)


# =========================================================
# RESPUESTA RAW
# =========================================================

print()
print("RESPUESTA RAW:")
print()


print(
    respuesta.text
)


# =========================================================
# ANALIZAR RESPUESTA
# =========================================================

if respuesta.status_code == 200:

    print()
    print("========================================")
    print("✅ JSEARCH FUNCIONA")
    print("========================================")


    try:

        datos = (
            respuesta.json()
        )

    except ValueError:

        print()
        print(
            "La respuesta no es JSON válido."
        )

        raise SystemExit(1)


    trabajos = datos.get(
        "data",
        []
    )


    print()
    print(
        "EMPLEOS RECIBIDOS:",
        len(trabajos)
    )


    # =====================================================
    # MOSTRAR ALGUNOS EMPLEOS
    # =====================================================

    for posicion, trabajo in enumerate(

        trabajos[:5],

        start=1

    ):

        print()
        print(
            f"[{posicion}]"
        )

        print(
            "Título:",
            trabajo.get(
                "job_title",
                ""
            )
        )

        print(
            "Empresa:",
            trabajo.get(
                "employer_name",
                ""
            )
        )

        print(
            "País:",
            trabajo.get(
                "job_country",
                ""
            )
        )

        print(
            "Ciudad:",
            trabajo.get(
                "job_city",
                ""
            )
        )

        print(
            "Remoto:",
            trabajo.get(
                "job_is_remote",
                False
            )
        )


elif respuesta.status_code == 403:

    print()
    print("========================================")
    print("❌ ERROR 403")
    print("========================================")


    print()
    print(
        "RapidAPI rechazó la solicitud."
    )


    print()
    print(
        "Respuesta:"
    )


    print(
        respuesta.text
    )


    print()
    print(
        "Esto significa que la API key utilizada"
    )


    print(
        "por este .env no tiene acceso a JSearch."
    )


elif respuesta.status_code == 401:

    print()
    print("========================================")
    print("❌ ERROR 401")
    print("========================================")


    print()
    print(
        "La API key no fue aceptada."
    )


elif respuesta.status_code == 429:

    print()
    print("========================================")
    print("⚠️ ERROR 429")
    print("========================================")


    print()
    print(
        "Se alcanzó un límite de solicitudes."
    )


else:

    print()
    print("========================================")
    print("❌ ERROR")
    print("========================================")


    print()
    print(
        "Código HTTP:",
        respuesta.status_code
    )


print()
print("========================================")
print("PRUEBA FINALIZADA")
print("========================================")