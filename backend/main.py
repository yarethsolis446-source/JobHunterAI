from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse

import os
import tempfile

import fitz

from services.app_service import AppService
from backend.reports.pdf_generator import PDFGenerator
from job_sources.job_history import JobHistory


# =========================================================
# APP
# =========================================================

app = FastAPI(
    title="JobHunter AI API",
    description=(
        "API para análisis de CV y "
        "recomendación de empleos"
    ),
    version="1.0.0"
)


# =========================================================
# SERVICIOS
# =========================================================

servicio = AppService()
pdf_generator = PDFGenerator()
historial = JobHistory()


# =========================================================
# NORMALIZAR FILTROS
# =========================================================

def normalizar_filtros(
    pais="",
    remoto=False
):

    # =====================================================
    # PAÍS
    # =====================================================

    if pais is None:

        pais_normalizado = None

    else:

        pais_normalizado = str(
            pais
        ).strip()

        if not pais_normalizado:

            pais_normalizado = None


    # =====================================================
    # REMOTO
    # =====================================================

    if isinstance(
        remoto,
        bool
    ):

        remoto_normalizado = remoto

    elif isinstance(
        remoto,
        str
    ):

        remoto_normalizado = (
            remoto.strip().lower()
            in (
                "true",
                "1",
                "yes",
                "si",
                "sí"
            )
        )

    else:

        remoto_normalizado = bool(
            remoto
        )


    return (
        pais_normalizado,
        remoto_normalizado
    )


# =========================================================
# INICIO
# =========================================================

@app.get("/")
def inicio():

    return {
        "mensaje":
            "JobHunter AI Backend funcionando"
    }


# =========================================================
# BUSCAR EMPLEOS
# =========================================================

@app.post("/jobs")
def jobs(

    consulta: str = "software developer",

    pais: str = "",

    remoto: bool = False

):

    try:

        print()
        print("==============================")
        print("ENDPOINT /jobs")
        print("==============================")


        # =================================================
        # NORMALIZAR FILTROS
        # =================================================

        pais_normalizado, remoto_normalizado = (
            normalizar_filtros(
                pais,
                remoto
            )
        )


        print()
        print("CONSULTA:")
        print(
            consulta
        )


        print()
        print("PAÍS RECIBIDO:")
        print(
            pais
            if pais
            else "Todos"
        )


        print()
        print("PAÍS NORMALIZADO:")
        print(
            pais_normalizado
            if pais_normalizado
            else "Todos"
        )


        print()
        print("REMOTO RECIBIDO:")
        print(
            remoto
        )


        print()
        print("REMOTO NORMALIZADO:")
        print(
            remoto_normalizado
        )


        # =================================================
        # BUSCAR EMPLEOS
        # =================================================

        empleos = servicio.buscar_empleos(

            consulta,

            pais=pais_normalizado,

            remoto=remoto_normalizado
        )


        # =================================================
        # RESPUESTA
        # =================================================

        return {

            "total":
                len(empleos),

            "filtros": {

                "pais":
                    pais_normalizado or "",

                "remoto":
                    remoto_normalizado
            },

            "empleos": [

                {

                    "job_id":
                        getattr(
                            empleo,
                            "job_id",
                            ""
                        ),

                    "titulo":
                        getattr(
                            empleo,
                            "titulo",
                            ""
                        ),

                    "empresa":
                        getattr(
                            empleo,
                            "empresa",
                            ""
                        ),

                    "descripcion":
                        getattr(
                            empleo,
                            "descripcion",
                            ""
                        ),

                    "habilidades":
                        getattr(
                            empleo,
                            "habilidades",
                            []
                        ),

                    "link":
                        getattr(
                            empleo,
                            "link",
                            ""
                        ),

                    "ubicacion":
                        getattr(
                            empleo,
                            "ubicacion",
                            ""
                        ),

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
                        getattr(
                            empleo,
                            "nivel",
                            "No especificado"
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
                        )
                }

                for empleo in empleos
            ]
        }


    except Exception as error:

        print()
        print(
            "ERROR BUSCANDO EMPLEOS:"
        )

        print(
            error
        )


        return {

            "error":
                "No se pudieron obtener los empleos",

            "detalle":
                str(error)
        }


# =========================================================
# ANALIZAR CV
# =========================================================

@app.post("/upload-cv")
async def subir_cv(

    archivo: UploadFile = File(...),

    # IMPORTANTE:
    # Como el PDF llega por multipart/form-data,
    # estos valores deben recibirse con Form().
    pais: str = Form(""),

    remoto: bool = Form(False)

):

    # =====================================================
    # NORMALIZAR FILTROS
    # =====================================================

    pais_normalizado, remoto_normalizado = (
        normalizar_filtros(
            pais,
            remoto
        )
    )


    print()
    print("==============================")
    print("ENDPOINT /upload-cv")
    print("==============================")


    print()
    print("PAÍS RECIBIDO:")
    print(
        pais
        if pais
        else "Todos"
    )


    print()
    print("PAÍS NORMALIZADO:")
    print(
        pais_normalizado
        if pais_normalizado
        else "Todos"
    )


    print()
    print("REMOTO RECIBIDO:")
    print(
        remoto
    )


    print()
    print("REMOTO NORMALIZADO:")
    print(
        remoto_normalizado
    )


    # =====================================================
    # VALIDAR ARCHIVO
    # =====================================================

    if not archivo.filename:

        return {

            "error":
                "No se recibió ningún archivo"
        }


    if not archivo.filename.lower().endswith(
        ".pdf"
    ):

        return {

            "error":
                "El archivo debe ser PDF"
        }


    contenido = await archivo.read()


    if not contenido:

        return {

            "error":
                "El archivo está vacío"
        }


    ruta = None


    # =====================================================
    # CREAR ARCHIVO TEMPORAL
    # =====================================================

    with tempfile.NamedTemporaryFile(

        delete=False,

        suffix=".pdf"

    ) as temporal:

        temporal.write(
            contenido
        )

        ruta = temporal.name


    try:

        # =================================================
        # EXTRAER TEXTO
        # =================================================

        texto = ""


        documento = fitz.open(
            ruta
        )


        for pagina in documento:

            texto_pagina = (
                pagina.get_text()
            )


            if texto_pagina:

                texto += (
                    texto_pagina
                    + "\n"
                )


        documento.close()


        if not texto.strip():

            return {

                "error":
                    "No se pudo extraer texto del PDF"
            }


        # =================================================
        # ANALIZAR CV
        # =================================================

        print()
        print("==============================")
        print("ANALIZANDO CV")
        print("==============================")


        candidato = (
            servicio.analizar_cv(
                texto
            )
        )


        # =================================================
        # RECOMENDAR EMPLEOS
        # =================================================

        print()
        print("==============================")
        print("GENERANDO RECOMENDACIONES")
        print("==============================")


        print(
            "Profesión:",
            candidato.profesion
        )


        print(
            "País:",
            pais_normalizado
            if pais_normalizado
            else "Todos"
        )


        print(
            "Solo remoto:",
            remoto_normalizado
        )


        recomendados = (
            servicio.recomendar_empleos(

                candidato,

                pais=pais_normalizado,

                remoto=remoto_normalizado
            )
        )


        # =================================================
        # PERFIL
        # =================================================

        perfil = {

            "profesion":
                candidato.profesion,

            "nivel":
                candidato.nivel,

            "experiencia":
                candidato.experiencia,

            "habilidades":
                candidato.habilidades,

            "idiomas":
                candidato.idiomas,

            "educacion":
                candidato.educacion
        }


        # =================================================
        # RESPUESTA
        # =================================================

        return {

            "mensaje":
                "CV analizado correctamente",

            "filtros": {

                "pais":
                    pais_normalizado or "",

                "remoto":
                    remoto_normalizado
            },

            "perfil":
                perfil,

            "total_empleos":
                len(recomendados),

            "empleos":
                recomendados
        }


    except Exception as error:

        print()
        print("==============================")
        print("ERROR ANALIZANDO CV")
        print("==============================")


        print(
            error
        )


        return {

            "error":
                "Ocurrió un error al analizar el CV",

            "detalle":
                str(error)
        }


    finally:

        # =================================================
        # ELIMINAR TEMPORAL
        # =================================================

        if (
            ruta
            and
            os.path.exists(
                ruta
            )
        ):

            os.remove(
                ruta
            )


# =========================================================
# HISTORIAL
# =========================================================

@app.get("/history")
def obtener_historial():

    try:

        empleos = (
            historial.obtener_todos()
        )


        return {

            "total":
                len(empleos),

            "empleos":
                empleos
        }


    except Exception as error:

        print(
            "ERROR OBTENIENDO HISTORIAL:",
            error
        )


        return {

            "error":
                "No se pudo obtener el historial",

            "detalle":
                str(error)
        }


# =========================================================
# EMPLEO DEL HISTORIAL
# =========================================================

@app.get("/history/{job_id}")
def obtener_empleo_historial(
    job_id: str
):

    try:

        empleo = (
            historial.buscar_por_id(
                job_id
            )
        )


        if empleo is None:

            return {

                "error":
                    "Empleo no encontrado"
            }


        return empleo


    except Exception as error:

        print(
            "ERROR OBTENIENDO EMPLEO:",
            error
        )


        return {

            "error":
                "No se pudo obtener el empleo",

            "detalle":
                str(error)
        }


# =========================================================
# GENERAR REPORTE PDF
# =========================================================

@app.post("/generate-report")
async def generar_reporte(

    archivo: UploadFile = File(...),

    # IMPORTANTE:
    # También es multipart/form-data.
    pais: str = Form(""),

    remoto: bool = Form(False)

):

    # =====================================================
    # NORMALIZAR FILTROS
    # =====================================================

    pais_normalizado, remoto_normalizado = (
        normalizar_filtros(
            pais,
            remoto
        )
    )


    print()
    print("==============================")
    print("ENDPOINT /generate-report")
    print("==============================")


    print(
        "País:",
        pais_normalizado
        if pais_normalizado
        else "Todos"
    )


    print(
        "Solo remoto:",
        remoto_normalizado
    )


    # =====================================================
    # VALIDAR ARCHIVO
    # =====================================================

    if not archivo.filename:

        return {

            "error":
                "No se recibió ningún archivo"
        }


    if not archivo.filename.lower().endswith(
        ".pdf"
    ):

        return {

            "error":
                "El archivo debe ser PDF"
        }


    contenido = await archivo.read()


    if not contenido:

        return {

            "error":
                "El archivo está vacío"
        }


    ruta_cv = None
    ruta_reporte = None


    # =====================================================
    # CV TEMPORAL
    # =====================================================

    with tempfile.NamedTemporaryFile(

        delete=False,

        suffix=".pdf"

    ) as temporal:

        temporal.write(
            contenido
        )

        ruta_cv = temporal.name


    # =====================================================
    # REPORTE TEMPORAL
    # =====================================================

    archivo_reporte = tempfile.NamedTemporaryFile(

        delete=False,

        suffix=".pdf"

    )


    ruta_reporte = (
        archivo_reporte.name
    )


    archivo_reporte.close()


    try:

        # =================================================
        # EXTRAER TEXTO
        # =================================================

        texto = ""


        documento = fitz.open(
            ruta_cv
        )


        for pagina in documento:

            texto_pagina = (
                pagina.get_text()
            )


            if texto_pagina:

                texto += (
                    texto_pagina
                    + "\n"
                )


        documento.close()


        if not texto.strip():

            return {

                "error":
                    "No se pudo extraer texto del CV"
            }


        # =================================================
        # ANALIZAR CV
        # =================================================

        candidato = (
            servicio.analizar_cv(
                texto
            )
        )


        # =================================================
        # RECOMENDAR EMPLEOS
        # =================================================

        recomendados = (
            servicio.recomendar_empleos(

                candidato,

                pais=pais_normalizado,

                remoto=remoto_normalizado
            )
        )


        # =================================================
        # PERFIL
        # =================================================

        perfil = {

            "profesion":
                candidato.profesion,

            "nivel":
                candidato.nivel,

            "experiencia":
                candidato.experiencia,

            "habilidades":
                candidato.habilidades,

            "idiomas":
                candidato.idiomas,

            "educacion":
                candidato.educacion
        }


        # =================================================
        # GENERAR PDF
        # =================================================

        resultado = pdf_generator.generar(

            ruta_reporte,

            perfil,

            recomendados
        )


        if not resultado:

            raise Exception(
                "PDFGenerator no pudo generar el reporte."
            )


        print()
        print("==============================")
        print("PDF GENERADO")
        print("==============================")


        return FileResponse(

            path=ruta_reporte,

            media_type="application/pdf",

            filename="JobHunter_AI_Reporte.pdf"
        )


    except Exception as error:

        print()
        print("==============================")
        print("ERROR GENERANDO PDF")
        print("==============================")


        print(
            error
        )


        if (
            ruta_reporte
            and
            os.path.exists(
                ruta_reporte
            )
        ):

            os.remove(
                ruta_reporte
            )


        return {

            "error":
                "No se pudo generar el reporte PDF",

            "detalle":
                str(error)
        }


    finally:

        # =================================================
        # ELIMINAR CV TEMPORAL
        # =================================================

        if (
            ruta_cv
            and
            os.path.exists(
                ruta_cv
            )
        ):

            os.remove(
                ruta_cv
            )