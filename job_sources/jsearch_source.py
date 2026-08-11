import requests

from models.job import Job


class JSearchSource:

    # =========================================================
    # INICIALIZAR
    # =========================================================

    def __init__(self, api_key):

        self.api_key = api_key

        self.url = (
            "https://jsearch.p.rapidapi.com/search"
        )

        print()
        print("==============================")
        print("JSEARCH SOURCE INICIALIZADA")
        print("==============================")

        if self.api_key:
            print("API KEY: CARGADA")
        else:
            print("API KEY: NO CARGADA")

        print(
            "URL:",
            self.url
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
        print("==============================")
        print("🔥 JSEARCH SOURCE")
        print("==============================")

        print(
            "Consulta:",
            consulta
        )

        print(
            "País:",
            pais if pais else "TODOS"
        )

        print(
            "Remoto:",
            remoto
        )

        # =====================================================
        # VALIDAR API KEY
        # =====================================================

        if not self.api_key:

            print()
            print(
                "❌ ERROR: JSEARCH_API_KEY NO EXISTE"
            )

            return []

        # =====================================================
        # CONSULTA
        # =====================================================

        consulta_final = (
            str(
                consulta
                or ""
            ).strip()
        )

        if not consulta_final:

            consulta_final = (
                "software developer"
            )

        # =====================================================
        # HEADERS
        # =====================================================

        headers = {

            "x-rapidapi-host":
                "jsearch.p.rapidapi.com",

            "x-rapidapi-key":
                self.api_key

        }

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
                fecha or "all"

        }

        # =====================================================
        # PAÍS
        # =====================================================

        pais_codigo = (
            self.convertir_pais(
                pais
            )
        )

        if pais_codigo:

            params["country"] = (
                pais_codigo.lower()
            )

        # =====================================================
        # REMOTO
        # =====================================================

        if remoto:

            params[
                "remote_jobs_only"
            ] = "true"

        # =====================================================
        # MOSTRAR REQUEST
        # =====================================================

        print()
        print(
            "PARAMETROS ENVIADOS A JSEARCH:"
        )

        print(
            params
        )

        print()
        print(
            "ENVIANDO REQUEST A RAPIDAPI..."
        )

        # =====================================================
        # REQUEST
        # =====================================================

        try:

            respuesta = requests.get(

                self.url,

                headers=headers,

                params=params,

                timeout=30

            )

        except requests.exceptions.Timeout:

            print()
            print(
                "❌ ERROR: TIMEOUT DE JSEARCH"
            )

            return []

        except requests.exceptions.RequestException as error:

            print()
            print(
                "❌ ERROR DE CONEXIÓN CON JSEARCH:"
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
            "STATUS HTTP:",
            respuesta.status_code
        )

        # =====================================================
        # RESPUESTA RAW
        # =====================================================

        print()
        print(
            "RESPUESTA DE RAPIDAPI:"
        )

        print(
            respuesta.text[:3000]
        )

        # =====================================================
        # ERRORES
        # =====================================================

        if respuesta.status_code == 401:

            print()
            print(
                "❌ ERROR 401: API KEY NO AUTORIZADA"
            )

            return []

        if respuesta.status_code == 403:

            print()
            print(
                "❌ ERROR 403: ACCESO DENEGADO"
            )

            print(
                "Respuesta:",
                respuesta.text
            )

            return []

        if respuesta.status_code == 404:

            print()
            print(
                "❌ ERROR 404: ENDPOINT NO ENCONTRADO"
            )

            return []

        if respuesta.status_code == 429:

            print()
            print(
                "❌ ERROR 429: LÍMITE DE SOLICITUDES"
            )

            return []

        if respuesta.status_code != 200:

            print()
            print(
                "❌ ERROR HTTP:",
                respuesta.status_code
            )

            return []

        # =====================================================
        # JSON
        # =====================================================

        try:

            datos = (
                respuesta.json()
            )

        except ValueError:

            print()
            print(
                "❌ ERROR: RESPUESTA JSON INVÁLIDA"
            )

            return []

        # =====================================================
        # VERIFICAR STATUS JSEARCH
        # =====================================================

        status_api = (
            datos.get(
                "status",
                ""
            )
        )

        print()
        print(
            "STATUS JSEARCH:",
            status_api
        )

        if status_api and status_api != "OK":

            print()
            print(
                "❌ JSEARCH DEVOLVIÓ ERROR:"
            )

            print(
                datos
            )

            return []

        # =====================================================
        # DATA
        # =====================================================

        trabajos = (
            datos.get(
                "data",
                []
            )
        )

        if not isinstance(
            trabajos,
            list
        ):

            print()
            print(
                "❌ ERROR: data NO ES UNA LISTA"
            )

            return []

        print()
        print(
            "================================"
        )

        print(
            "EMPLEOS RECIBIDOS DE JSEARCH:",
            len(trabajos)
        )

        print(
            "================================"
        )

        # =====================================================
        # MOSTRAR EMPLEOS CRUDOS
        # =====================================================

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
                "Estado:",
                oferta.get(
                    "job_state"
                )
            )

            print(
                "Remoto:",
                oferta.get(
                    "job_is_remote"
                )
            )

        # =====================================================
        # CONVERTIR A JOB
        # =====================================================

        empleos = []

        for oferta in trabajos:

            if not isinstance(
                oferta,
                dict
            ):

                continue

            try:

                empleo = (
                    self.convertir_job(
                        oferta
                    )
                )

                empleos.append(
                    empleo
                )

            except Exception as error:

                print()
                print(
                    "❌ ERROR CONVIRTIENDO EMPLEO:"
                )

                print(
                    error
                )

        # =====================================================
        # FILTRO LOCAL DE PAÍS
        # =====================================================

        if pais_codigo:

            print()
            print(
                "================================"
            )

            print(
                "FILTRO LOCAL DE PAÍS"
            )

            print(
                "================================"
            )

            filtrados = []

            for empleo in empleos:

                pais_empleo = (
                    self.normalizar_codigo_pais(
                        getattr(
                            empleo,
                            "pais",
                            ""
                        )
                    )
                )

                if pais_empleo == pais_codigo:

                    filtrados.append(
                        empleo
                    )

                else:

                    print(
                        "Descartado por país:",
                        empleo.titulo,
                        "|",
                        pais_empleo,
                        "!=",
                        pais_codigo
                    )

            empleos = filtrados

        # =====================================================
        # FILTRO LOCAL REMOTO
        # =====================================================

        if remoto:

            print()
            print(
                "================================"
            )

            print(
                "FILTRO LOCAL REMOTO"
            )

            print(
                "================================"
            )

            filtrados = []

            for empleo in empleos:

                if self.convertir_bool(
                    getattr(
                        empleo,
                        "remoto",
                        False
                    )
                ):

                    filtrados.append(
                        empleo
                    )

                else:

                    print(
                        "Descartado por no ser remoto:",
                        empleo.titulo
                    )

            empleos = filtrados

        # =====================================================
        # RESULTADO
        # =====================================================

        print()
        print(
            "================================"
        )

        print(
            "RESULTADO JSEARCH"
        )

        print(
            "================================"
        )

        print(
            "Total final:",
            len(empleos)
        )

        for empleo in empleos:

            print(
                "-",
                empleo.titulo,
                "|",
                empleo.empresa,
                "|",
                empleo.pais,
                "| remoto:",
                empleo.remoto
            )

        return empleos

    # =========================================================
    # CONVERTIR OFERTA A JOB
    # =========================================================

    def convertir_job(
        self,
        oferta
    ):

        # =====================================================
        # ID
        # =====================================================

        job_id = (
            oferta.get(
                "job_id"
            )
            or ""
        )

        # =====================================================
        # TÍTULO
        # =====================================================

        titulo = (
            oferta.get(
                "job_title"
            )
            or "Puesto sin especificar"
        )

        # =====================================================
        # EMPRESA
        # =====================================================

        empresa = (
            oferta.get(
                "employer_name"
            )
            or "Empresa no especificada"
        )

        # =====================================================
        # DESCRIPCIÓN
        # =====================================================

        descripcion = (
            oferta.get(
                "job_description"
            )
            or ""
        )

        # =====================================================
        # LINK
        # =====================================================

        link = (
            oferta.get(
                "job_apply_link"
            )
            or oferta.get(
                "job_google_link"
            )
            or ""
        )

        # =====================================================
        # UBICACIÓN
        # =====================================================

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

        pais_original = (
            oferta.get(
                "job_country"
            )
            or ""
        )

        ubicacion_original = (
            oferta.get(
                "job_location"
            )
            or ""
        )

        # =====================================================
        # PAÍS
        # =====================================================

        pais = (
            self.detectar_pais(
                pais_original,
                ciudad,
                estado,
                ubicacion_original,
                descripcion,
                empresa
            )
        )

        # =====================================================
        # UBICACIÓN FINAL
        # =====================================================

        partes = []

        if ciudad:

            partes.append(
                str(
                    ciudad
                ).strip()
            )

        if estado:

            partes.append(
                str(
                    estado
                ).strip()
            )

        if pais:

            partes.append(
                pais
            )

        if not partes and ubicacion_original:

            partes.append(
                str(
                    ubicacion_original
                ).strip()
            )

        ubicacion = (
            ", ".join(
                partes
            )
        )

        # =====================================================
        # REMOTO
        # =====================================================

        remoto = self.convertir_bool(

            oferta.get(
                "job_is_remote",
                False
            )

        )

        # =====================================================
        # DETECTAR REMOTO POR TEXTO
        # =====================================================

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
                    ubicacion_original
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

        if any(

            palabra in texto_remoto

            for palabra in indicadores_remoto

        ):

            remoto = True

        # =====================================================
        # TIPO DE EMPLEO
        # =====================================================

        tipo_empleo = (
            oferta.get(
                "job_employment_type"
            )
            or ""
        )

        # =====================================================
        # SALARIO
        # =====================================================

        salario = ""

        salario_minimo = (
            oferta.get(
                "job_min_salary"
            )
        )

        salario_maximo = (
            oferta.get(
                "job_max_salary"
            )
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

        # =====================================================
        # HABILIDADES
        # =====================================================

        habilidades = []

        habilidades_api = (
            oferta.get(
                "job_required_skills"
            )
        )

        if isinstance(
            habilidades_api,
            list
        ):

            habilidades = [

                str(
                    habilidad
                ).strip()

                for habilidad
                in habilidades_api

                if habilidad

            ]

        # =====================================================
        # EXTRAER HABILIDADES DEL TEXTO
        # =====================================================

        if not habilidades:

            habilidades = (
                self.detectar_habilidades(
                    titulo,
                    descripcion
                )
            )

        # =====================================================
        # EXPERIENCIA
        # =====================================================

        experiencia = 0

        experiencia_api = (
            oferta.get(
                "job_required_experience"
            )
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
                        float(
                            meses
                        )
                        / 12
                    )

                except (
                    ValueError,
                    TypeError
                ):

                    experiencia = 0

        # =====================================================
        # NIVEL
        # =====================================================

        nivel = (
            self.detectar_nivel(
                titulo,
                descripcion,
                experiencia_api
            )
        )

        # =====================================================
        # IDIOMA
        # =====================================================

        idioma = (
            oferta.get(
                "job_language"
            )
            or ""
        )

        # =====================================================
        # CREAR JOB
        # =====================================================

        return Job(

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

            remoto=remoto,

            pais=pais,

            tipo_empleo=tipo_empleo

        )

    # =========================================================
    # DETECTAR HABILIDADES
    # =========================================================

    def detectar_habilidades(
        self,
        titulo,
        descripcion
    ):

        texto = (

            str(
                titulo
                or ""
            )
            + " "
            +
            str(
                descripcion
                or ""
            )

        ).lower()

        habilidades_posibles = [

            "python",
            "java",
            "javascript",
            "typescript",
            "c++",
            "c#",
            ".net",
            "php",
            "ruby",
            "go",
            "rust",

            "react",
            "angular",
            "vue",
            "node.js",
            "node",

            "sql",
            "mysql",
            "postgresql",
            "mongodb",

            "aws",
            "azure",
            "gcp",

            "docker",
            "kubernetes",

            "git",
            "github",

            "api",
            "rest",

            "machine learning",
            "artificial intelligence",
            "ai",

            "html",
            "css",

            "linux"

        ]

        encontradas = []

        for habilidad in habilidades_posibles:

            if habilidad in texto:

                encontradas.append(
                    habilidad
                )

        return encontradas

    # =========================================================
    # DETECTAR NIVEL
    # =========================================================

    def detectar_nivel(
        self,
        titulo,
        descripcion,
        experiencia
    ):

        texto = (

            str(
                titulo
                or ""
            )
            + " "
            +
            str(
                descripcion
                or ""
            )

        ).lower()

        if any(

            palabra in texto

            for palabra in [

                "intern",
                "internship",
                "entry level",
                "entry-level",
                "junior",
                "jr."

            ]

        ):

            return "Junior"

        if any(

            palabra in texto

            for palabra in [

                "senior",
                "sr.",
                "lead",
                "principal",
                "staff"

            ]

        ):

            return "Senior"

        if any(

            palabra in texto

            for palabra in [

                "mid level",
                "mid-level",
                "midlevel",
                "associate"

            ]

        ):

            return "Mid"

        if isinstance(
            experiencia,
            dict
        ):

            meses = (
                experiencia.get(
                    "required_experience_in_months"
                )
            )

            try:

                if meses is not None:

                    anos = (
                        float(
                            meses
                        )
                        / 12
                    )

                    if anos < 2:

                        return "Junior"

                    if anos < 5:

                        return "Mid"

                    return "Senior"

            except (
                ValueError,
                TypeError
            ):

                pass

        return "No especificado"

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
                    "remoto",
                    "remota"

                }

            )

        if isinstance(
            valor,
            int
        ):

            return valor != 0

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
        # PAÍS DIRECTO
        # =====================================================

        if pais:

            codigo = (
                self.convertir_pais(
                    pais
                )
            )

            if codigo:

                return codigo

        # =====================================================
        # TEXTO
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
            "limon"

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
            "united states of america",
            "usa",
            "u.s.a.",
            "u.s."

        ]

        if any(

            indicador in texto

            for indicador
            in indicadores_us

        ):

            return "US"

        # =====================================================
        # CIUDADES ESTADOUNIDENSES
        # =====================================================

        ciudades_us = [

            "washington",
            "new york",
            "los angeles",
            "chicago",
            "houston",
            "seattle",
            "boston",
            "austin",
            "denver",
            "miami",
            "san francisco",
            "san diego",
            "atlanta",
            "dallas",
            "phoenix",
            "mclean",
            "arlington",
            "new jersey"

        ]

        if any(

            ciudad_us in texto

            for ciudad_us
            in ciudades_us

        ):

            return "US"

        # =====================================================
        # CANADÁ
        # =====================================================

        if any(

            indicador in texto

            for indicador
            in [

                "canada",
                "canadá",
                "toronto",
                "vancouver",
                "montreal"

            ]

        ):

            return "CA"

        # =====================================================
        # MÉXICO
        # =====================================================

        if any(

            indicador in texto

            for indicador
            in [

                "mexico",
                "méxico",
                "cdmx",
                "ciudad de mexico",
                "ciudad de méxico"

            ]

        ):

            return "MX"

        # =====================================================
        # COLOMBIA
        # =====================================================

        if any(

            indicador in texto

            for indicador
            in [

                "colombia",
                "bogotá",
                "bogota",
                "medellín",
                "medellin"

            ]

        ):

            return "CO"

        # =====================================================
        # ESPAÑA
        # =====================================================

        if any(

            indicador in texto

            for indicador
            in [

                "españa",
                "espana",
                "madrid",
                "barcelona"

            ]

        ):

            return "ES"

        # =====================================================
        # ARGENTINA
        # =====================================================

        if any(

            indicador in texto

            for indicador
            in [

                "argentina",
                "buenos aires"

            ]

        ):

            return "AR"

        # =====================================================
        # CHILE
        # =====================================================

        if any(

            indicador in texto

            for indicador
            in [

                "chile",
                "santiago"

            ]

        ):

            return "CL"

        # =====================================================
        # BRASIL
        # =====================================================

        if any(

            indicador in texto

            for indicador
            in [

                "brazil",
                "brasil",
                "são paulo",
                "sao paulo"

            ]

        ):

            return "BR"

        # =====================================================
        # SIN DETERMINAR
        # =====================================================

        return ""

    # =========================================================
    # CONVERTIR PAÍS
    # =========================================================

    def convertir_pais(
        self,
        pais
    ):

        if not pais:

            return None

        pais_normalizado = (

            str(
                pais
            )
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
            "u.s.": "US",

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
            "brazil": "BR",
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

    # =========================================================
    # NORMALIZAR CÓDIGO DE PAÍS
    # =========================================================

    def normalizar_codigo_pais(
        self,
        pais
    ):

        if not pais:

            return ""

        codigo = (
            self.convertir_pais(
                pais
            )
        )

        return (
            codigo
            or ""
        )