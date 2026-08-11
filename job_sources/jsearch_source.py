import requests

from models.job import Job


class JSearchSource:

    def __init__(self, api_key):

        self.api_key = api_key

        self.url = (
            "https://jsearch.p.rapidapi.com/search"
        )

        print()
        print("==============================")
        print("JSEARCH SOURCE INICIALIZADA")
        print("==============================")

        print(
            "URL:",
            self.url
        )

        print(
            "API KEY:",
            "CARGADA" if self.api_key else "NO CARGADA"
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
        print("JSEARCH SOURCE")
        print("==============================")

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
        # VALIDAR API KEY
        # =====================================================

        if not self.api_key:

            print()
            print(
                "ERROR: JSEARCH_API_KEY ESTÁ VACÍA"
            )

            return []


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
        # NORMALIZAR REMOTO
        # =====================================================

        remoto = self.convertir_bool(
            remoto
        )


        # =====================================================
        # CONSULTA
        # =====================================================

        consulta_final = (
            str(
                consulta
                or ""
            )
            .strip()
        )


        if not consulta_final:

            consulta_final = (
                "software developer"
            )


        # =====================================================
        # SI ES REMOTO
        # =====================================================

        if remoto:

            consulta_final = (
                f"{consulta_final} remote"
            )


        print(
            "Consulta final:",
            consulta_final
        )


        # =====================================================
        # HEADERS
        # =====================================================

        headers = {

            "x-rapidapi-host":
                "jsearch.p.rapidapi.com",

            "x-rapidapi-key":
                self.api_key,

            "Accept":
                "application/json"
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
                "1"
        }


        # =====================================================
        # FECHA
        # =====================================================

        if fecha:

            params["date_posted"] = fecha


        # =====================================================
        # PAIS
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


        # =====================================================
        # MOSTRAR PETICION
        # =====================================================

        print()
        print("==============================")
        print("PETICIÓN A JSEARCH")
        print("==============================")


        print(
            "URL:",
            self.url
        )


        print(
            "PARAMETROS:",
            params
        )


        print(
            "HEADERS:",
            {
                "x-rapidapi-host":
                    headers["x-rapidapi-host"],

                "x-rapidapi-key":
                    "***OCULTA***",

                "Accept":
                    headers["Accept"]
            }
        )


        # =====================================================
        # REQUEST
        # =====================================================

        try:

            print()
            print(
                "ENVIANDO REQUEST A RAPIDAPI..."
            )


            respuesta = requests.get(

                self.url,

                headers=headers,

                params=params,

                timeout=30

            )


            print(
                "REQUEST TERMINADO"
            )


        except requests.exceptions.Timeout:

            print()
            print(
                "ERROR: TIMEOUT DE JSEARCH"
            )

            return []


        except requests.exceptions.ConnectionError as error:

            print()
            print(
                "ERROR DE CONEXIÓN CON JSEARCH"
            )

            print(
                error
            )

            return []


        except requests.exceptions.RequestException as error:

            print()
            print(
                "ERROR REQUEST JSEARCH"
            )

            print(
                error
            )

            return []


        except Exception as error:

            print()
            print(
                "ERROR DESCONOCIDO HACIENDO REQUEST"
            )

            print(
                type(error).__name__
            )

            print(
                error
            )

            return []


        # =====================================================
        # STATUS
        # =====================================================

        print()
        print("==============================")
        print("RESPUESTA JSEARCH")
        print("==============================")


        print(
            "STATUS HTTP:",
            respuesta.status_code
        )


        print(
            "URL FINAL:",
            respuesta.url
        )


        # =====================================================
        # RESPUESTA RAW
        # =====================================================

        print()
        print(
            "RESPUESTA RAW:"
        )


        print(
            respuesta.text[:3000]
        )


        # =====================================================
        # ERRORES HTTP
        # =====================================================

        if respuesta.status_code == 401:

            print()
            print(
                "ERROR 401"
            )

            print(
                "La API key no está autorizada."
            )

            return []


        if respuesta.status_code == 403:

            print()
            print(
                "ERROR 403"
            )

            print(
                "RapidAPI rechazó la petición."
            )

            return []


        if respuesta.status_code == 404:

            print()
            print(
                "ERROR 404"
            )

            print(
                "Endpoint de JSearch no encontrado."
            )

            return []


        if respuesta.status_code == 429:

            print()
            print(
                "ERROR 429"
            )

            print(
                "Límite de peticiones alcanzado."
            )

            return []


        if respuesta.status_code != 200:

            print()
            print(
                "ERROR HTTP:",
                respuesta.status_code
            )

            return []


        # =====================================================
        # JSON
        # =====================================================

        try:

            datos = respuesta.json()

        except ValueError as error:

            print()
            print(
                "ERROR: JSEARCH NO DEVOLVIÓ JSON"
            )

            print(
                error
            )

            return []


        # =====================================================
        # MOSTRAR ESTRUCTURA
        # =====================================================

        print()
        print("==============================")
        print("JSON JSEARCH")
        print("==============================")


        print(
            "Tipo:",
            type(datos).__name__
        )


        if isinstance(datos, dict):

            print(
                "Keys:",
                list(
                    datos.keys()
                )
            )


        # =====================================================
        # STATUS API
        # =====================================================

        api_status = datos.get(
            "status"
        )


        print(
            "Status API:",
            api_status
        )


        # =====================================================
        # PARAMETROS API
        # =====================================================

        parametros_api = datos.get(
            "parameters",
            {}
        )


        print()
        print(
            "PARAMETROS RECIBIDOS POR JSEARCH:"
        )


        print(
            parametros_api
        )


        # =====================================================
        # DATA
        # =====================================================

        trabajos = datos.get(
            "data",
            []
        )


        if trabajos is None:

            trabajos = []


        if not isinstance(
            trabajos,
            list
        ):

            print()
            print(
                "ERROR: data NO ES UNA LISTA"
            )

            print(
                "Tipo:",
                type(trabajos).__name__
            )

            return []


        print()
        print("==============================")
        print("RESULTADOS JSEARCH")
        print("==============================")


        print(
            "Empleos recibidos:",
            len(trabajos)
        )


        # =====================================================
        # SI NO HAY RESULTADOS
        # =====================================================

        if len(trabajos) == 0:

            print()
            print(
                "JSEARCH RESPONDIÓ CORRECTAMENTE"
            )

            print(
                "PERO NO DEVOLVIÓ EMPLEOS."
            )

            return []


        # =====================================================
        # MOSTRAR OFERTAS
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
                f"[OFERTA {posicion}]"
            )


            print(
                "ID:",
                oferta.get(
                    "job_id"
                )
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
            # DETECTAR PAIS
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


            if pais_oferta:

                partes.append(
                    pais_oferta
                )


            if not partes and job_location:

                partes.append(
                    str(
                        job_location
                    ).strip()
                )


            ubicacion = ", ".join(
                partes
            )


            # =================================================
            # REMOTO
            # =================================================

            remoto_oferta = (
                self.convertir_bool(

                    oferta.get(
                        "job_is_remote",
                        False
                    )

                )
            )


            # =================================================
            # DETECTAR REMOTO POR TEXTO
            # =================================================

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

                for palabra
                in indicadores_remoto

            ):

                remoto_oferta = True


            # =================================================
            # TIPO
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


            # =================================================
            # HABILIDADES
            # =================================================

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

                    str(x).strip()

                    for x in habilidades_api

                    if x

                ]


            # =================================================
            # EXPERIENCIA
            # =================================================

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
        # FILTRO LOCAL PAIS
        # =====================================================

        if pais_codigo:

            print()
            print("==============================")
            print("FILTRO LOCAL DE PAIS")
            print("==============================")


            filtrados = []


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

                    filtrados.append(
                        empleo
                    )

                else:

                    print(

                        "DESCARTADO POR PAIS:",

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
            print("==============================")
            print("FILTRO LOCAL REMOTO")
            print("==============================")


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

                        "DESCARTADO POR NO SER REMOTO:",

                        empleo.titulo

                    )


            empleos = filtrados


        # =====================================================
        # RESULTADO FINAL
        # =====================================================

        print()
        print("==============================")
        print("JSEARCH FINALIZADO")
        print("==============================")


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
    # DETECTAR PAIS
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
        # PAIS DIRECTO
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

        if any(

            x in texto

            for x in [

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

        ):

            return "CR"


        # =====================================================
        # ESTADOS UNIDOS
        # =====================================================

        if any(

            x in texto

            for x in [

                "united states",
                "usa",
                "u.s."

            ]

        ):

            return "US"


        # =====================================================
        # CANADA
        # =====================================================

        if any(

            x in texto

            for x in [

                "canada",
                "canadá"

            ]

        ):

            return "CA"


        # =====================================================
        # MEXICO
        # =====================================================

        if any(

            x in texto

            for x in [

                "mexico",
                "méxico",
                "cdmx"

            ]

        ):

            return "MX"


        # =====================================================
        # COLOMBIA
        # =====================================================

        if any(

            x in texto

            for x in [

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

            x in texto

            for x in [

                "españa",
                "espana",
                "madrid",
                "barcelona"

            ]

        ):

            return "ES"


        return ""


    # =========================================================
    # CONVERTIR PAIS
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