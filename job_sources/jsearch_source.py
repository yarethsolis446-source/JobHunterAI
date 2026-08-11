import requests

from models.job import Job


class JSearchSource:

    def __init__(self, api_key):

        self.api_key = api_key

        self.url = (
            "https://jsearch.p.rapidapi.com/search"
        )

        print()
        print("========================================")
        print("🔥🔥🔥 JSEARCH SOURCE INICIALIZADA 🔥🔥🔥")
        print("========================================")

        print(
            "API KEY:",
            "CARGADA" if self.api_key else "VACÍA"
        )

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
        print("========================================")
        print("🔥🔥🔥 JSEARCH NUEVO CÓDIGO 🔥🔥🔥")
        print("========================================")

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
            print("❌ ERROR: API KEY VACÍA")

            return []


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
            str(consulta)
            if consulta
            else "software developer"
        )


        # =====================================================
        # PARÁMETROS
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

        if pais:

            pais_codigo = (
                self.convertir_pais(
                    pais
                )
            )

            if pais_codigo:

                params["country"] = (
                    pais_codigo
                )


        # =====================================================
        # REMOTO
        # =====================================================

        if remoto:

            params["remote_jobs_only"] = "true"


        print()
        print("========================================")
        print("PARAMETROS ENVIADOS A JSEARCH")
        print("========================================")

        print(
            params
        )


        # =====================================================
        # INFORMACIÓN REQUEST
        # =====================================================

        print()
        print("========================================")
        print("ENVIANDO REQUEST A RAPIDAPI...")
        print("========================================")

        print(
            "URL:",
            self.url
        )

        print(
            "METHOD: GET"
        )

        print(
            "HEADERS:"
        )

        print(
            {
                "x-rapidapi-host":
                    "jsearch.p.rapidapi.com",

                "x-rapidapi-key":
                    "********",

                "Content-Type":
                    "application/json"
            }
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


            print()
            print("========================================")
            print("🔥🔥🔥 RESPUESTA DE RAPIDAPI 🔥🔥🔥")
            print("========================================")


            print(
                "STATUS HTTP:",
                respuesta.status_code
            )


            print(
                "URL FINAL:",
                respuesta.url
            )


            print(
                "HEADERS RESPUESTA:"
            )

            print(
                dict(
                    respuesta.headers
                )
            )


            print()
            print("========================================")
            print("RESPUESTA RAW")
            print("========================================")


            print(
                respuesta.text[:10000]
            )


        except requests.exceptions.Timeout as error:

            print()
            print("========================================")
            print("❌ TIMEOUT RAPIDAPI")
            print("========================================")

            print(
                repr(error)
            )

            return []


        except requests.exceptions.ConnectionError as error:

            print()
            print("========================================")
            print("❌ ERROR DE CONEXIÓN RAPIDAPI")
            print("========================================")

            print(
                repr(error)
            )

            return []


        except requests.exceptions.RequestException as error:

            print()
            print("========================================")
            print("❌ ERROR REQUEST RAPIDAPI")
            print("========================================")

            print(
                repr(error)
            )

            return []


        except Exception as error:

            print()
            print("========================================")
            print("❌ ERROR INESPERADO REQUEST")
            print("========================================")

            print(
                type(error).__name__
            )

            print(
                repr(error)
            )

            return []


        # =====================================================
        # STATUS
        # =====================================================

        if respuesta.status_code != 200:

            print()
            print("========================================")
            print("❌ JSEARCH DEVOLVIÓ ERROR")
            print("========================================")

            print(
                "STATUS:",
                respuesta.status_code
            )

            print(
                "BODY:",
                respuesta.text[:10000]
            )

            return []


        # =====================================================
        # JSON
        # =====================================================

        try:

            datos = (
                respuesta.json()
            )

        except ValueError as error:

            print()
            print("========================================")
            print("❌ JSON INVÁLIDO")
            print("========================================")

            print(
                repr(error)
            )

            print(
                respuesta.text[:10000]
            )

            return []


        # =====================================================
        # MOSTRAR INFORMACIÓN API
        # =====================================================

        print()
        print("========================================")
        print("INFORMACIÓN JSEARCH")
        print("========================================")


        print(
            "Status:",
            datos.get(
                "status"
            )
        )


        print(
            "Request ID:",
            datos.get(
                "request_id"
            )
        )


        print(
            "Parameters:"
        )

        print(
            datos.get(
                "parameters",
                {}
            )
        )


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

            print(
                "❌ DATA NO ES UNA LISTA"
            )

            print(
                "DATA:",
                trabajos
            )

            return []


        print()
        print("========================================")
        print("RESULTADOS JSEARCH")
        print("========================================")


        print(
            "Total recibidos:",
            len(trabajos)
        )


        # =====================================================
        # SI NO HAY RESULTADOS
        # =====================================================

        if not trabajos:

            print()
            print(
                "⚠️ JSEARCH RESPONDIÓ CORRECTAMENTE"
            )

            print(
                "⚠️ PERO NO DEVOLVIÓ EMPLEOS"
            )

            print()
            print(
                "JSON COMPLETO:"
            )

            print(
                datos
            )

            return []


        # =====================================================
        # CONVERTIR
        # =====================================================

        empleos = []


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
                f"========== OFERTA {posicion} =========="
            )


            titulo = (
                oferta.get(
                    "job_title"
                )
                or "Puesto sin especificar"
            )


            empresa = (
                oferta.get(
                    "employer_name"
                )
                or "Empresa no especificada"
            )


            job_id = (
                oferta.get(
                    "job_id"
                )
                or ""
            )


            descripcion = (
                oferta.get(
                    "job_description"
                )
                or ""
            )


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


            remoto_oferta = (
                self.convertir_bool(
                    oferta.get(
                        "job_is_remote",
                        False
                    )
                )
            )


            print(
                "ID:",
                job_id
            )

            print(
                "Título:",
                titulo
            )

            print(
                "Empresa:",
                empresa
            )

            print(
                "País:",
                pais_oferta
            )

            print(
                "Ciudad:",
                ciudad
            )

            print(
                "Ubicación:",
                job_location
            )

            print(
                "Remoto:",
                remoto_oferta
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

                    str(
                        habilidad
                    ).strip()

                    for habilidad
                    in habilidades_api

                    if habilidad

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
                            float(meses)
                            / 12
                        )

                    except (
                        ValueError,
                        TypeError
                    ):

                        experiencia = 0


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
            # TIPO
            # =================================================

            tipo_empleo = (
                oferta.get(
                    "job_employment_type"
                )
                or ""
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
            # PAÍS
            # =================================================

            pais_final = (
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
            # UBICACIÓN
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


            if pais_final:

                partes.append(
                    pais_final
                )


            if (
                not partes
                and
                job_location
            ):

                partes.append(
                    str(
                        job_location
                    ).strip()
                )


            ubicacion = (
                ", ".join(
                    partes
                )
            )


            # =================================================
            # JOB
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

                nivel="No especificado",

                job_id=job_id,

                remoto=remoto_oferta,

                pais=pais_final,

                tipo_empleo=tipo_empleo

            )


            empleos.append(
                empleo
            )


        # =====================================================
        # FILTRO PAÍS
        # =====================================================

        if pais:

            pais_codigo = (
                self.convertir_pais(
                    pais
                )
            )


            print()
            print("========================================")
            print("FILTRO PAÍS")
            print("========================================")


            print(
                "Buscando:",
                pais_codigo
            )


            filtrados = []


            for empleo in empleos:

                if (
                    self.convertir_pais(
                        empleo.pais
                    )
                    ==
                    pais_codigo
                ):

                    filtrados.append(
                        empleo
                    )

                else:

                    print(
                        "DESCARTADO:",
                        empleo.titulo,
                        "|",
                        empleo.pais
                    )


            empleos = filtrados


        # =====================================================
        # FILTRO REMOTO
        # =====================================================

        if remoto:

            print()
            print("========================================")
            print("FILTRO REMOTO")
            print("========================================")


            empleos = [

                empleo

                for empleo
                in empleos

                if self.convertir_bool(
                    empleo.remoto
                )

            ]


        # =====================================================
        # RESULTADO
        # =====================================================

        print()
        print("========================================")
        print("JSEARCH RESULTADO FINAL")
        print("========================================")


        print(
            "Total:",
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
    # BOOLEANO
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

        if any(

            palabra in texto

            for palabra
            in [

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
        # USA
        # =====================================================

        if any(

            palabra in texto

            for palabra
            in [

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

            palabra in texto

            for palabra
            in [

                "canada",
                "canadá"

            ]

        ):

            return "CA"


        # =====================================================
        # MEXICO
        # =====================================================

        if any(

            palabra in texto

            for palabra
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

            palabra in texto

            for palabra
            in [

                "colombia",
                "bogota",
                "bogotá",
                "medellin",
                "medellín"

            ]

        ):

            return "CO"


        # =====================================================
        # ESPAÑA
        # =====================================================

        if any(

            palabra in texto

            for palabra
            in [

                "españa",
                "espana",
                "madrid",
                "barcelona"

            ]

        ):

            return "ES"


        return ""


    # =========================================================
    # CONVERTIR PAÍS
    # =========================================================

    def convertir_pais(
        self,
        pais
    ):

        if not pais:

            return ""


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