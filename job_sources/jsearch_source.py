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
        print("🔥 JSEARCH SOURCE INICIALIZADA")
        print("========================================")

        print(
            "API KEY:",
            "CARGADA" if self.api_key else "NO CARGADA"
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

            "x-rapidapi-key":
                self.api_key,

            "x-rapidapi-host":
                "jsearch.p.rapidapi.com",

            "Content-Type":
                "application/json"
        }


        # =====================================================
        # CONSULTA
        # =====================================================

        consulta_final = (
            str(consulta or "")
            .strip()
        )


        if not consulta_final:

            consulta_final = (
                "software developer"
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


        print()
        print("========================================")
        print("PARAMETROS ENVIADOS A JSEARCH")
        print("========================================")

        print(
            params
        )


        print()
        print("========================================")
        print("ENVIANDO REQUEST A RAPIDAPI...")
        print("========================================")


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
            print("❌ REQUEST TIMEOUT")

            return []


        except requests.exceptions.ConnectionError as error:

            print()
            print("❌ ERROR DE CONEXIÓN")

            print(
                error
            )

            return []


        except requests.exceptions.RequestException as error:

            print()
            print("❌ ERROR REQUEST")

            print(
                error
            )

            return []


        except Exception as error:

            print()
            print("❌ ERROR DESCONOCIDO REQUEST")

            print(
                error
            )

            return []


        # =====================================================
        # RESPUESTA RAW
        # =====================================================

        print()
        print("========================================")
        print("🔥🔥🔥 RESPUESTA DE RAPIDAPI 🔥🔥🔥")
        print("========================================")


        print()
        print("STATUS:")

        print(
            respuesta.status_code
        )


        print()
        print("URL FINAL:")

        print(
            respuesta.url
        )


        print()
        print("RESPUESTA RAW:")

        print(
            respuesta.text[:10000]
        )


        # =====================================================
        # HEADERS RESPUESTA
        # =====================================================

        print()
        print("HEADERS DE RESPUESTA:")

        print(
            dict(
                respuesta.headers
            )
        )


        # =====================================================
        # ERRORES HTTP
        # =====================================================

        if respuesta.status_code == 401:

            print()
            print("❌ ERROR 401")

            print(
                "API KEY NO AUTORIZADA"
            )

            return []


        if respuesta.status_code == 403:

            print()
            print("❌ ERROR 403")

            print(
                "ACCESO DENEGADO / API NO SUSCRITA"
            )

            return []


        if respuesta.status_code == 404:

            print()
            print("❌ ERROR 404")

            print(
                "ENDPOINT NO ENCONTRADO"
            )

            return []


        if respuesta.status_code == 429:

            print()
            print("❌ ERROR 429")

            print(
                "LÍMITE DE SOLICITUDES ALCANZADO"
            )

            return []


        if respuesta.status_code != 200:

            print()
            print("❌ JSEARCH DEVOLVIÓ ERROR")

            print(
                respuesta.text[:5000]
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
            print("❌ RESPUESTA JSON INVÁLIDA")

            return []


        # =====================================================
        # STATUS JSEARCH
        # =====================================================

        print()
        print("========================================")
        print("INFORMACIÓN JSEARCH")
        print("========================================")


        print(
            "Status API:",
            datos.get(
                "status"
            )
        )


        print(
            "Mensaje API:",
            datos.get(
                "message",
                ""
            )
        )


        print(
            "Request ID:",
            datos.get(
                "request_id",
                ""
            )
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
                "❌ DATA NO ES UNA LISTA"
            )

            print(
                type(trabajos)
            )

            return []


        print()
        print("========================================")
        print("EMPLEOS RECIBIDOS")
        print("========================================")


        print(
            "Total:",
            len(trabajos)
        )


        # =====================================================
        # SI NO HAY RESULTADOS
        # =====================================================

        if not trabajos:

            print()
            print(
                "⚠️ JSEARCH RESPONDIÓ 200 PERO NO DEVOLVIÓ EMPLEOS"
            )

            return []


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
                "Remoto:",
                oferta.get(
                    "job_is_remote"
                )
            )


            print(
                "ID:",
                oferta.get(
                    "job_id"
                )
            )


        # =====================================================
        # CONVERTIR EMPLEOS
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
            # TÍTULO
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
            # PAÍS
            # =================================================

            pais_detectado = (
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


            if pais_detectado:

                partes.append(
                    pais_detectado
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

                for palabra in indicadores_remoto

            ):

                remoto_oferta = True


            # =================================================
            # TIPO EMPLEO
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

            try:

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

                    pais=pais_detectado,

                    tipo_empleo=tipo_empleo

                )


                empleos.append(
                    empleo
                )


            except Exception as error:

                print()
                print(
                    "❌ ERROR CREANDO JOB:"
                )

                print(
                    error
                )


        # =====================================================
        # FILTRO LOCAL PAÍS
        # =====================================================

        if pais_codigo:

            print()
            print("========================================")
            print("FILTRO LOCAL DE PAÍS")
            print("========================================")


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

                        "DESCARTADO POR PAÍS:",

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
            print("========================================")
            print("FILTRO LOCAL REMOTO")
            print("========================================")


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
        # RESULTADO
        # =====================================================

        print()
        print("========================================")
        print("🔥 RESULTADO JSEARCH")
        print("========================================")


        print(
            "Empleos convertidos:",
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

            "limon",

            "santo domingo"

        ]


        if any(

            indicador in texto

            for indicador in indicadores_cr

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

            for indicador in indicadores_us

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

            for indicador in indicadores_ca

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

            for indicador in indicadores_mx

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

            for indicador in indicadores_co

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

            for indicador in indicadores_es

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