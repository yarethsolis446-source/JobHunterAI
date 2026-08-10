from services.cv_service import CVService
from engine.search_engine import SearchEngine



ruta = r"C:\Users\Admin\Documents\Beatbren oroginal.pdf"



# Leer CV

candidato = CVService().procesar_cv(
    ruta
)



# Crear buscador

engine = SearchEngine()



# Buscar empleos filtrando por idioma

resultados = engine.buscar(

    candidato,

    idioma="inglés"

)



print("\n=========== RESULTADOS ===========\n")



for resultado in resultados:


    print(
        resultado.empleo.titulo
    )


    print(
        "Empresa:",
        resultado.empleo.empresa
    )


    print(
        "Compatibilidad:",
        resultado.score,
        "%"
    )


    print(
        "Fuente:",
        resultado.fuente
    )


    print(
        "Coincidencias:",
        resultado.coincidencias
    )


    print(
        "Faltantes:",
        resultado.faltantes
    )


    print(
        "-" * 40
    )