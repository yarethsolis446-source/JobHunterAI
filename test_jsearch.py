import os

from dotenv import load_dotenv

from job_sources.jsearch_source import JSearchSource


load_dotenv()


api_key = os.getenv("RAPIDAPI_KEY")


if not api_key:
    print("ERROR: No existe RAPIDAPI_KEY")
    exit()


print("API Key cargada correctamente")


buscador = JSearchSource(api_key)


print("\nBuscando empleos...\n")


resultados = buscador.buscar_empleos(
    "developer jobs in chicago"
)


print("\n======================")
print("RESULTADOS FINALES")
print("======================")


print("Cantidad:", len(resultados))


for empleo in resultados:

    print("----------------------")

    print("Titulo:")
    print(empleo.titulo)

    print("Empresa:")
    print(empleo.empresa)

    print("Link:")
    print(empleo.link)