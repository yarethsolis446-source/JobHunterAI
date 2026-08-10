
import requests

from models.job import Job


class JSearchSource:

    def __init__(self, api_key):

        self.api_key = api_key

        self.url = (
            "https://jsearch.p.rapidapi.com/search"
        )

    # =========================================================
    # BUSCAR EMPLEOS
    # =========================================================

    def buscar_empleos(
        self,
        consulta,
        fecha="all",
        pais=None,
        remoto=False
    ):

        print()
        print("==========================")
        print("JSEARCH SOURCE")
        print("==========================")

        print(
            "Consulta:",
            consulta
        )

        print(
            "País:",
            pais if pais else "TODOS LOS PAISES"
        )

        print(
            "Solo remoto:",
            remoto
        )

        # =====================================================
        # NORMALIZAR PAÍS
        # =====================================================

        pais_codigo = self.convertir_pais(
            pais
        )

        print(
            "Código de país:",
            pais_codigo or "TODOS"
        )

        # =====================================================
        # HEADERS
        # =====================================================

        headers = {

            "x-rapidapi-host":
                "jsearch.p.rapidapi.com",

            "x-rapidapi-key":
                self.api_key,

            "Content-Type":
                "application/json"
        }

        # =====================================================
        # CONSULTA
        # =====================================================

        consulta_final = (
            consulta
            or ""
        )

        # Cuando el usuario pide remoto,
        # ampliamos la consulta para aumentar
        # la posibilidad de encontrar ofertas remotas.
        #
        # IMPORTANTE:
        # Esto NO convierte automáticamente una oferta
        # en remota. Más abajo verificamos la oferta.

        if remoto:

            consulta_final = (
                f"{consulta_final} remote"
            )

        # =====================================================
        # PARAMETROS
        # =====================================================

        params = {

            "query":
                consulta_final,

            "page":
                "1",

            "num_pages":
                "1",

            "date_posted":
                fecha
        }

        # =====================================================
        # PAÍS
        # =====================================================

        if pais_codigo:

            params["country"] = (
                pais_codigo
            )

        # =====================================================
        # REMOTO
        # =====================================================

        if remoto:

            params[
                "remote_jobs_only"
            ] = "true"

        print()
        print(
            "PARAMETROS ENVIADOS A JSEARCH:"
        )

        print(
            params
        )

        # =====================================================
        # PETICIÓN
        # =====================================================

        try:

            respuesta = requests.get(

                self.url,

                headers=headers,

                params=params,

                timeout=20
            )

        except requests.exceptions.Timeout:

            print()
            print(
                "ERROR: Tiempo de espera agotado"
            )

            return []

        except requests.exceptions.RequestException as error:

            print()
            print(
                "ERROR DE CONEXION:"
            )

            print(
                error
            )

            return []

        # =====================================================
        # STATUS
        # =====================================================

        print()
        print(
            "STATUS HTTP:"
        )

        print(
            respuesta.status_code
        )

        # =====================================================
        # ERRORES HTTP
        # =====================================================

        if respuesta.status_code == 401:

            print(
                "ERROR 401: API KEY NO AUTORIZADA"
            )

            return []

        if respuesta.status_code == 403:

            print(
                "ERROR 403: ACCESO DENEGADO"
            )

            return []

        if respuesta.status_code == 404:

            print(
                "ERROR 404: ENDPOINT NO ENCONTRADO"
            )

            return []

        if respuesta.status_code != 200:

            print(
                "ERROR: La API no respondió correctamente"
            )

            print(
                respuesta.text[:1000]
            )

            return []

        # =====================================================
        # JSON
        # =====================================================

        try:

            datos = respuesta.json()

        except ValueError:

            print()
            print(
                "ERROR: Respuesta JSON inválida"
            )

            return []

        # =====================================================
        # INFORMACIÓN API
        # =====================================================

        parametros_api = datos.get(
            "parameters",
            {}
        )

        print()
        print("==========================")
        print("INFORMACION DE JSEARCH")
        print("==========================")

        print(
            "Country:",
            parametros_api.get(
                "country",
                "Todos"
            )
        )

        print(
            "Remote:",
            parametros_api.get(
                "remote_jobs_only",
                False
            )
        )

        # =====================================================
        # DATA
        # =====================================================

        trabajos = datos.get(
            "data",
            []
        )

        if not isinstance(
            trabajos,
            list
        ):

            trabajos = []

        print(
            "Empleos recibidos:",
            len(trabajos)
        )

        # =====================================================
        # MOSTRAR DATOS CRUDOS
        # =====================================================

        print()
        print("==========================")
        print("DATOS RECIBIDOS DE JSEARCH")
        print("==========================")

        for posicion, oferta in enumerate(
            trabajos,
            start=1
        ):

            if not isinstance(
                oferta,
                dict
            ):

                continue

            print()
            print(
                f"[{posicion}]"
            )

            print(
                "Título:",
                oferta.get(
                    "job_title"
                )
            )

            print(
                "Empresa:",
                oferta.get(
                    "employer_name"
                )
            )

            print(
                "País:",
                oferta.get(
                    "job_country"
                )
            )

            print(
                "Ciudad:",
                oferta.get(
                    "job_city"
                )
            )

            print(
                "Remoto:",
                oferta.get(
                    "job_is_remote"
                )
            )

            print(
                "Ubicación:",
                oferta.get(
                    "job_location"
                )
            )

        # =====================================================
        # CONVERTIR
        # =====================================================

        empleos = []

        for oferta in trabajos:

            if not isinstance(
                oferta,
                dict
            ):

                continue

            # =================================================
            # ID
            # =================================================

            job_id = (
                oferta.get(
                    "job_id"
                )
                or ""
            )

            # =================================================
            # TITULO
            # =================================================

            titulo = (
                oferta.get(
                    "job_title"
                )
                or "Puesto sin especificar"
            )

            # =================================================
            # EMPRESA
            # =================================================

            empresa = (
                oferta.get(
                    "employer_name"
                )
                or "Empresa no especificada"
            )

            # =================================================
            # DESCRIPCIÓN
            # =================================================

            descripcion = (
                oferta.get(
                    "job_description"
                )
                or ""
            )

            # =================================================
            # LINK
            # =================================================

            link = (

                oferta.get(
                    "job_apply_link"
                )

                or

                oferta.get(
                    "job_google_link"
                )

                or ""

            )

            # =================================================
            # UBICACIÓN
            # =================================================

            ciudad = (
                oferta.get(
                    "job_city"
                )
                or ""
            )

            estado = (
                oferta.get(
                    "job_state"
                )
                or ""
            )

            pais_oferta = (
                oferta.get(
                    "job_country"
                )
                or ""
            )

            job_location = (
                oferta.get(
                    "job_location"
                )
                or ""
            )

            # =================================================
            # DETECTAR PAÍS
            # =================================================

            pais_oferta = (
                self.detectar_pais(
                    pais_oferta,
                    ciudad,
                    estado,
                    job_location,
                    descripcion,
                    empresa
                )
            )

            # =================================================
            # UBICACIÓN FINAL
            # =================================================

            partes = []

            if ciudad:

                partes.append(
                    str(ciudad).strip()
                )

            if estado:

                partes.append(
                    str(estado).strip()
                )

            if pais_oferta:

                partes.append(
                    pais_oferta
                )

            if not partes and job_location:

                partes.append(
                    str(job_location).strip()
                )

            ubicacion = ", ".join(
                partes
            )

            # =================================================
            # REMOTO
            # =================================================

            remoto_oferta = (
                oferta.get(
                    "job_is_remote",
                    False
                )
            )

            remoto_oferta = (
                self.convertir_bool(
                    remoto_oferta
                )
            )

            # =================================================
            # VERIFICAR REMOTO POR TEXTO
            # =================================================
            #
            # Si JSearch devuelve False pero el título,
            # ubicación o descripción contienen evidencia
            # explícita de trabajo remoto, podemos reconocerlo.
            #
            # NO usamos palabras como "flexible" o "híbrido"
            # como remoto.

            texto_remoto = " ".join(

                [

                    str(
                        titulo
                        or ""
                    ),

                    str(
                        descripcion
                        or ""
                    ),

                    str(
                        job_location
                        or ""
                    )

                ]

            ).lower()

            indicadores_remoto = [

                "remote",

                "remoto",

                "remota",

                "trabajo remoto",

                "teletrabajo",

                "teletrabajo",

                "work from home",

                "work-from-home",

                "working from home",

                "home based",

                "home-based",

                "fully remote",

                "100% remote",

                "remote position",

                "remote job",

                "virtual position"

            ]

            evidencia_remota = any(

                palabra in texto_remoto

                for palabra
                in indicadores_remoto

            )

            if evidencia_remota:

                remoto_oferta = True

            # =================================================
            # TIPO DE EMPLEO
            # =================================================

            tipo_empleo = (
                oferta.get(
                    "job_employment_type"
                )
                or ""
            )

            # =================================================
            # SALARIO
            # =================================================

            salario = ""

            salario_minimo = oferta.get(
                "job_min_salary"
            )

            salario_maximo = oferta.get(
                "job_max_salary"
            )

            salario_periodo = (
                oferta.get(
                    "job_salary_period"
                )
                or ""
            )

            if (
                salario_minimo is not None
                and
                salario_maximo is not None
            ):

                salario = (

                    f"{salario_minimo} - "
                    f"{salario_maximo}"

                )

            elif salario_minimo is not None:

                salario = str(
                    salario_minimo
                )

            elif salario_maximo is not None:

                salario = str(
                    salario_maximo
                )

            if (
                salario
                and
                salario_periodo
            ):

                salario += (
                    f" / {salario_periodo}"
                )

            # =================================================
            # HABILIDADES
            # =================================================

            habilidades = []

            habilidades_api = oferta.get(
                "job_required_skills"
            )

            if isinstance(
                habilidades_api,
                list
            ):

                habilidades = [

                    str(x).strip()

                    for x in habilidades_api

                    if x

                ]

            # =================================================
            # EXPERIENCIA
            # =================================================

            experiencia = 0

            experiencia_api = oferta.get(
                "job_required_experience"
            )

            if isinstance(
                experiencia_api,
                dict
            ):

                meses = (
                    experiencia_api.get(
                        "required_experience_in_months"
                    )
                )

                if meses is not None:

                    try:

                        experiencia = (
                            float(meses)
                            / 12
                        )

                    except (
                        ValueError,
                        TypeError
                    ):

                        experiencia = 0

            # =================================================
            # NIVEL
            # =================================================

            nivel = (
                "No especificado"
            )

            # =================================================
            # IDIOMA
            # =================================================

            idioma = (
                oferta.get(
                    "job_language"
                )
                or ""
            )

            # =================================================
            # CREAR JOB
            # =================================================

            empleo = Job(

                titulo=titulo,

                empresa=empresa,

                descripcion=descripcion,

                habilidades=habilidades,

                experiencia=experiencia,

                link=link,

                ubicacion=ubicacion,

                salario=salario,

                idioma=idioma,

                nivel=nivel,

                job_id=job_id,

                remoto=remoto_oferta,

                pais=pais_oferta,

                tipo_empleo=tipo_empleo

            )

            empleos.append(
                empleo
            )

        # =====================================================
        # FILTRO LOCAL DE PAÍS
        # =====================================================

        if pais_codigo:

            print()
            print(
                "=========================="
            )

            print(
                "FILTRO LOCAL DE PAÍS"
            )

            print(
                "=========================="
            )

            empleos_filtrados = []

            for empleo in empleos:

                pais_empleo = (

                    str(

                        getattr(
                            empleo,
                            "pais",
                            ""
                        )

                        or ""

                    )
                    .strip()
                    .upper()

                )

                if pais_empleo == pais_codigo:

                    empleos_filtrados.append(
                        empleo
                    )

                else:

                    print(

                        "DESCARTADO POR PAÍS:",

                        empleo.titulo,

                        "|",

                        pais_empleo,

                        "!=",

                        pais_codigo

                    )

            empleos = (
                empleos_filtrados
            )

        # =====================================================
        # FILTRO LOCAL REMOTO
        # =====================================================

        if remoto:

            print()
            print(
                "=========================="
            )

            print(
                "FILTRO LOCAL REMOTO"
            )

            print(
                "=========================="
            )

            empleos_filtrados = []

            for empleo in empleos:

                es_remoto = (
                    self.convertir_bool(
                        getattr(
                            empleo,
                            "remoto",
                            False
                        )
                    )
                )

                if es_remoto:

                    empleos_filtrados.append(
                        empleo
                    )

                else:

                    print(

                        "DESCARTADO POR NO SER REMOTO:",

                        empleo.titulo

                    )

            empleos = (
                empleos_filtrados
            )

        # =====================================================
        # RESULTADO
        # =====================================================

        print()
        print(
            "=========================="
        )

        print(
            "EMPLEOS DESPUÉS DE FILTROS"
        )

        print(
            "=========================="
        )

        print(
            "Total:",
            len(empleos)
        )

        for empleo in empleos:

            print(

                "-",

                empleo.titulo,

                "| País:",

                empleo.pais,

                "| Remoto:",

                empleo.remoto

            )

        return empleos

    # =========================================================
    # CONVERTIR BOOLEANO
    # =========================================================

    def convertir_bool(
        self,
        valor
    ):

        if isinstance(
            valor,
            bool
        ):

            return valor

        if isinstance(
            valor,
            str
        ):

            return (
                valor.strip().lower()
                in {
                    "true",
                    "1",
                    "yes",
                    "si",
                    "sí",
                    "remote",
                    "remoto"
                }
            )

        return bool(
            valor
        )

    # =========================================================
    # DETECTAR PAÍS
    # =========================================================

    def detectar_pais(
        self,
        pais,
        ciudad,
        estado,
        ubicacion,
        descripcion,
        empresa
    ):

        # =====================================================
        # 1. PAÍS DIRECTO DE JSEARCH
        # =====================================================

        if pais:

            codigo = self.convertir_pais(
                pais
            )

            if codigo:

                return codigo

        # =====================================================
        # TEXTO PARA DETECCIÓN
        # =====================================================

        texto = " ".join(

            [

                str(
                    pais
                    or ""
                ),

                str(
                    ciudad
                    or ""
                ),

                str(
                    estado
                    or ""
                ),

                str(
                    ubicacion
                    or ""
                ),

                str(
                    descripcion
                    or ""
                ),

                str(
                    empresa
                    or ""
                )

            ]

        ).lower()

        # =====================================================
        # COSTA RICA
        # =====================================================

        indicadores_cr = [

            "costa rica",

            "san josé",

            "san jose",

            "heredia",

            "alajuela",

            "cartago",

            "puntarenas",

            "guanacaste",

            "limón",

            "limon",

            "santo domingo"

        ]

        if any(

            indicador in texto

            for indicador
            in indicadores_cr

        ):

            return "CR"

        # =====================================================
        # ESTADOS UNIDOS
        # =====================================================

        indicadores_us = [

            "united states",

            "usa",

            "u.s.",

            "us"

        ]

        if any(

            indicador in texto

            for indicador
            in indicadores_us

        ):

            return "US"

        # =====================================================
        # CANADÁ
        # =====================================================

        indicadores_ca = [

            "canada",

            "canadá"

        ]

        if any(

            indicador in texto

            for indicador
            in indicadores_ca

        ):

            return "CA"

        # =====================================================
        # MÉXICO
        # =====================================================

        indicadores_mx = [

            "mexico",

            "méxico",

            "cdmx",

            "ciudad de méxico",

            "ciudad de mexico"

        ]

        if any(

            indicador in texto

            for indicador
            in indicadores_mx

        ):

            return "MX"

        # =====================================================
        # COLOMBIA
        # =====================================================

        indicadores_co = [

            "colombia",

            "bogotá",

            "bogota",

            "medellín",

            "medellin"

        ]

        if any(

            indicador in texto

            for indicador
            in indicadores_co

        ):

            return "CO"

        # =====================================================
        # ESPAÑA
        # =====================================================

        indicadores_es = [

            "españa",

            "espana",

            "madrid",

            "barcelona"

        ]

        if any(

            indicador in texto

            for indicador
            in indicadores_es

        ):

            return "ES"

        # =====================================================
        # SI NO SE PUEDE DETERMINAR
        # =====================================================

        return ""

    # =========================================================
    # CONVERTIR PAÍS A CÓDIGO
    # =========================================================

    def convertir_pais(
        self,
        pais
    ):

        if not pais:

            return None

        pais_normalizado = (

            str(pais)
            .strip()
            .lower()

        )

        paises = {

            "costa rica": "CR",
            "cr": "CR",

            "estados unidos": "US",
            "usa": "US",
            "eeuu": "US",
            "us": "US",

            "canada": "CA",
            "canadá": "CA",
            "ca": "CA",

            "mexico": "MX",
            "méxico": "MX",
            "mx": "MX",

            "españa": "ES",
            "espana": "ES",
            "es": "ES",

            "colombia": "CO",
            "co": "CO",

            "argentina": "AR",
            "ar": "AR",

            "chile": "CL",
            "cl": "CL",

            "brasil": "BR",
            "br": "BR",

            "peru": "PE",
            "perú": "PE",
            "pe": "PE",

            "panama": "PA",
            "panamá": "PA",
            "pa": "PA",

            "guatemala": "GT",
            "gt": "GT",

            "el salvador": "SV",
            "sv": "SV",

            "honduras": "HN",
            "hn": "HN",

            "nicaragua": "NI",
            "ni": "NI",

            "reino unido": "GB",
            "uk": "GB",
            "gb": "GB",

            "alemania": "DE",
            "de": "DE",

            "francia": "FR",
            "fr": "FR",

            "italia": "IT",
            "it": "IT",

            "japon": "JP",
            "japón": "JP",
            "jp": "JP",

            "australia": "AU",
            "au": "AU"
        }

        return paises.get(

            pais_normalizado,

            pais_normalizado.upper()

        )

