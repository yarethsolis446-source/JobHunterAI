import os
from pathlib import Path

from dotenv import load_dotenv

from ai.cv_analyzer import CVAnalyzer
from ai.job_matcher import JobMatcher

from job_sources.aggregator import JobAggregator
from job_sources.jsearch_source import JSearchSource

from job_sources.job_history import JobHistory


# =========================================================
# CARGAR VARIABLES DE ENTORNO
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[1]

ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)


# =========================================================
# API KEY
# =========================================================

JSEARCH_API_KEY = os.getenv(
    "JSEARCH_API_KEY"
)


if not JSEARCH_API_KEY:

    raise Exception(
        f"No se encontró JSEARCH_API_KEY en: {ENV_PATH}"
    )


print()
print("==============================")
print("CONFIGURACIÓN")
print("==============================")


print(
    "API Key cargada correctamente."
)


# =========================================================
# APP SERVICE
# =========================================================

class AppService:

    def __init__(self):

        # =================================================
        # CV
        # =================================================

        self.cv_analyzer = CVAnalyzer()


        # =================================================
        # MATCHER
        # =================================================

        self.job_matcher = JobMatcher()


        # =================================================
        # HISTORIAL
        # =================================================

        self.job_history = JobHistory()


        # =================================================
        # AGREGADOR
        # =================================================

        self.aggregator = JobAggregator()


        # =================================================
        # JSEARCH
        # =================================================

        self.aggregator.agregar_fuente(

            JSearchSource(
                JSEARCH_API_KEY
            )

        )


        print(
            "Fuente JSearch configurada"
        )


        print(
            "AppService iniciado correctamente."
        )


    # =====================================================
    # BUSCAR EMPLEOS
    # =====================================================

    def buscar_empleos(
        self,
        consulta=None,
        pais=None,
        remoto=False
    ):

        print()
        print("==============================")
        print("BUSCANDO EMPLEOS")
        print("==============================")


        print(
            "Consulta:",
            consulta
        )


        print(
            "País:",
            pais if pais else "Todos"
        )


        print(
            "Solo remoto:",
            remoto
        )


        # =================================================
        # BUSCAR
        # =================================================

        empleos = (
            self.aggregator.obtener_empleos(

                consulta,

                pais=pais,

                remoto=remoto

            )
        )


        print()
        print(
            "TOTAL OBTENIDOS:",
            len(empleos)
        )


        return empleos


    # =====================================================
    # ANALIZAR CV
    # =====================================================

    def analizar_cv(
        self,
        texto
    ):

        print()
        print("==============================")
        print("ANALIZANDO CV")
        print("==============================")


        candidato = (
            self.cv_analyzer.analizar(
                texto
            )
        )


        print(
            "Profesión:",
            candidato.profesion
        )


        print(
            "Nivel:",
            candidato.nivel
        )


        print(
            "Experiencia:",
            candidato.experiencia
        )


        print(
            "Habilidades:",
            candidato.habilidades
        )


        return candidato


    # =====================================================
    # RECOMENDAR EMPLEOS
    # =====================================================

    def recomendar_empleos(
        self,
        candidato,
        pais=None,
        remoto=False
    ):

        print()
        print("==============================")
        print("GENERANDO RECOMENDACIONES")
        print("==============================")


        print(
            "Profesión detectada:",
            candidato.profesion
        )


        print(
            "País:",
            pais if pais else "Todos"
        )


        print(
            "Solo remoto:",
            remoto
        )


        # =================================================
        # CONSULTA
        # =================================================

        consulta = candidato.profesion


        # =================================================
        # BUSCAR
        # =================================================

        empleos = self.buscar_empleos(

            consulta,

            pais=pais,

            remoto=remoto

        )


        print()
        print(
            "Empleos encontrados:",
            len(empleos)
        )


        resultados = []


        # =================================================
        # ANALIZAR EMPLEOS
        # =================================================

        for empleo in empleos:

            try:

                print()
                print("------------------------------")


                print(
                    "Analizando:",
                    empleo.titulo
                )


                print(
                    "Empresa:",
                    empleo.empresa
                )


                print(
                    "ID:",
                    empleo.job_id
                )


                # =================================================
                # MATCH
                # =================================================

                resultado = (
                    self.job_matcher.analizar(

                        candidato,

                        empleo

                    )
                )


                # =================================================
                # RESULTADO
                # =================================================

                resultado_empleo = {

                    "job_id":
                    empleo.job_id,

                    "titulo":
                    empleo.titulo,

                    "empresa":
                    empleo.empresa,

                    "descripcion":
                    empleo.descripcion,

                    "habilidades":
                    getattr(
                        empleo,
                        "habilidades",
                        []
                    ),

                    "link":
                    empleo.link,

                    "ubicacion":
                    empleo.ubicacion,

                    "salario":
                    getattr(
                        empleo,
                        "salario",
                        ""
                    ),

                    "idioma":
                    getattr(
                        empleo,
                        "idioma",
                        ""
                    ),

                    "experiencia":
                    getattr(
                        empleo,
                        "experiencia",
                        0
                    ),

                    "nivel":
                    resultado.get(
                        "nivel",
                        getattr(
                            empleo,
                            "nivel",
                            "No especificado"
                        )
                    ),

                    "remoto":
                    getattr(
                        empleo,
                        "remoto",
                        False
                    ),

                    "pais":
                    getattr(
                        empleo,
                        "pais",
                        ""
                    ),

                    "tipo_empleo":
                    getattr(
                        empleo,
                        "tipo_empleo",
                        ""
                    ),

                    "score":
                    resultado.get(
                        "score",
                        0
                    ),

                    "modalidad":
                    resultado.get(
                        "modalidad",
                        ""
                    ),

                    "coincidencias":
                    resultado.get(
                        "coincidencias",
                        []
                    ),

                    "faltantes":
                    resultado.get(
                        "faltantes",
                        []
                    ),

                    "explicacion":
                    resultado.get(
                        "explicacion",
                        []
                    )
                }


                resultados.append(
                    resultado_empleo
                )


                # =================================================
                # HISTORIAL
                # =================================================

                guardado = (
                    self.job_history.add(
                        resultado_empleo
                    )
                )


                if guardado:

                    print(
                        "Nuevo empleo guardado:",
                        empleo.titulo
                    )

                else:

                    print(
                        "Empleo ya existía:",
                        empleo.titulo
                    )


            except Exception as error:

                print()
                print(
                    "=============================="
                )


                print(
                    "ERROR ANALIZANDO EMPLEO:"
                )


                print(
                    getattr(
                        empleo,
                        "titulo",
                        "Título desconocido"
                    )
                )


                print(
                    "ERROR:"
                )


                print(
                    error
                )


                print(
                    "=============================="
                )


        # =================================================
        # ORDENAR
        # =================================================

        resultados.sort(

            key=lambda x: x.get(
                "score",
                0
            ),

            reverse=True

        )


        # =================================================
        # MOSTRAR
        # =================================================

        print()
        print("==============================")
        print("EMPLEOS RECOMENDADOS")
        print("==============================")


        print(
            "Total:",
            len(resultados)
        )


        for posicion, empleo in enumerate(
            resultados,
            start=1
        ):

            print(

                f"{posicion}. "
                f"{empleo['titulo']} - "
                f"{empleo['empresa']} - "
                f"{empleo['score']}% - "
                f"{empleo['pais']} - "
                f"Remoto: {empleo['remoto']}"

            )


        print()
        print("==============================")
        print("PROCESO FINALIZADO")
        print("==============================")


        return resultados