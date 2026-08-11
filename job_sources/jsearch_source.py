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
        print("JSEARCH SOURCE INICIALIZADA")
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
            print("❌ ERROR: JSEARCH_API_KEY ESTÁ VACÍA")

            return []


        # =====================================================
        # NORMALIZAR PAÍS
        # =====================================================

        pais_codigo = self.convertir_pais(
            pais
        )


        print(
            "Código país:",
            pais_codigo if pais_codigo else "TODOS"
        )


        # =====================================================
        # NORMALIZAR CONSULTA
        # =====================================================

        consulta_final = (
            str(consulta or "").strip()
        )


        if not consulta_final:

            consulta_final = "software developer"


        # =====================================================
        # IMPORTANTE
        # =====================================================
        #
        # NO agregamos "remote" a la consulta.
        #
        # El filtro remoto se manda mediante
        # remote_jobs_only.
        #

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
        # HEADERS
        # =====================================================

        headers = {

            "x-rapidapi-host":
                "jsearch.p.rapidapi.com",

            "x-rapidapi-key":
                self.api_key,

            "Content-Type":
                "application/json",

            "Accept":
                "application/json"
        }


        # =====================================================
        # MOSTRAR REQUEST
        # =====================================================

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
            print("❌ ERROR: TIMEOUT DE JSEARCH")

            return []


        except requests.exceptions.ConnectionError as error:

            print()
            print("❌ ERROR DE CONEXIÓN CON JSEARCH")
            print(
                error
            )

            return []


        except requests.exceptions.RequestException as error:

            print()
            print("❌ ERROR REQUEST JSEARCH")

            print(
                error
            )

            return []


        except Exception as error:

            print()
            print("❌ ERROR INESPERADO REQUEST")

            print(
                error
            )

            return []


        # =====================================================
        # RESPUESTA REAL
        # =====================================================

        print()
        print("========================================")
        print("🔥🔥🔥 RESPUESTA REAL DE JSEARCH 🔥🔥🔥")
        print("========================================")

        print(
            "STATUS:",
            respuesta.status_code
        )

        print()
        print(
            "URL FINAL:",
            respuesta.url
        )

        print()
        print(
            "RESPUESTA:"
        )

        print(
            respuesta.text[:10000]
        )

        print()
        print("========================================")


        # =====================================================
        # ERRORES HTTP
        # =====================================================

        if respuesta.status_code == 401:

            print()
            print("❌ ERROR 401")
            print("API KEY NO AUTORIZADA")

            return []


        if respuesta.status_code == 403:

            print()
            print("❌ ERROR 403")
            print("ACCESO DENEGADO")

            try:

                error_json = (
                    respuesta.json()
                )

                print(
                    "DETALLE:",
                    error_json
                )

            except Exception:

                pass

            return []


        if respuesta.status_code == 404:

            print()
            print("❌ ERROR 404")
            print("ENDPOINT NO ENCONTRADO")

            return []


        if respuesta.status_code == 429:

            print()
            print("❌ ERROR 429")
            print("LÍMITE DE REQUESTS ALCANZADO")

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
            print("❌ ERROR: JSEARCH NO DEVOLVIÓ JSON")

            return []


        # =====================================================
        # STATUS API
        # =====================================================

        print()
        print("========================================")
        print("INFORMACIÓN DE JSEARCH")
        print("========================================")

        print(
            "Status API:",
            datos.get(
                "status",
                "NO ESPECIFICADO"
            )
        )


        if "message" in datos:

            print(
                "Mensaje:",
                datos.get(
                    "message"
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

            print()
            print(
                "❌ ERROR: data NO ES UNA LISTA"
            )

            print(
                type(trabajos)
            )

            return []


        print()
        print(
            "EMPLEOS RECIBIDOS:",
            len(trabajos)
        )


        # =====================================================
        # SI NO HAY EMPLEOS
        # =====================================================

        if not trabajos:

            print()
            print("⚠️ JSEARCH RESPONDIÓ CORRECTAMENTE")
            print("⚠️ PERO NO DEVOLVIÓ EMPLEOS")

            return []


        # =====================================================
        # MOSTRAR EMPLEOS CRUDOS
        # =====================================================

        print()
        print("========================================")
        print("EMPLEOS RECIBIDOS DE JSEARCH")
        print("========================================")


        for posicion, oferta in enumerate(

            trabajos[:10],

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
        # CONVERTIR A JOB
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


            pais_oferta_api = (
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

            pais_oferta = (
                self.detectar_pais(

                    pais_oferta_api,

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
        # FILTRO LOCAL DE PAÍS
        # =====================================================

        if pais_codigo:

            print()
            print("========================================")
            print("FILTRO LOCAL DE PAÍS")
            print("========================================")


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
            print("========================================")
            print("FILTRO LOCAL REMOTO")
            print("========================================")


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
        print("========================================")
        print("RESULTADO JSEARCH")
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

                "| País:",

                empleo.pais,

                "| Remoto:",

                empleo.remoto

            )


        print()
        print("========================================")
        print("JSEARCH FINALIZADO")
        print("========================================")


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
        # ARGENTINA
        # =====================================================

        indicadores_ar = [

            "argentina",

            "buenos aires"

        ]


        if any(

            indicador in texto

            for indicador
            in indicadores_ar

        ):

            return "AR"


        # =====================================================
        # CHILE
        # =====================================================

        indicadores_cl = [

            "chile",

            "santiago"

        ]


        if any(

            indicador in texto

            for indicador
            in indicadores_cl

        ):

            return "CL"


        # =====================================================
        # BRASIL
        # =====================================================

        indicadores_br = [

            "brazil",

            "brasil",

            "são paulo",

            "sao paulo",

            "rio de janeiro"

        ]


        if any(

            indicador in texto

            for indicador
            in indicadores_br

        ):

            return "BR"


        # =====================================================
        # PERÚ
        # =====================================================

        indicadores_pe = [

            "peru",

            "perú",

            "lima"

        ]


        if any(

            indicador in texto

            for indicador
            in indicadores_pe

        ):

            return "PE"


        # =====================================================
        # PANAMÁ
        # =====================================================

        indicadores_pa = [

            "panama",

            "panamá"

        ]


        if any(

            indicador in texto

            for indicador
            in indicadores_pa

        ):

            return "PA"


        # =====================================================
        # GUATEMALA
        # =====================================================

        if "guatemala" in texto:

            return "GT"


        # =====================================================
        # HONDURAS
        # =====================================================

        if "honduras" in texto:

            return "HN"


        # =====================================================
        # NICARAGUA
        # =====================================================

        if "nicaragua" in texto:

            return "NI"


        # =====================================================
        # REINO UNIDO
        # =====================================================

        indicadores_gb = [

            "united kingdom",

            "uk",

            "england",

            "london"

        ]


        if any(

            indicador in texto

            for indicador
            in indicadores_gb

        ):

            return "GB"


        # =====================================================
        # ALEMANIA
        # =====================================================

        indicadores_de = [

            "germany",

            "alemania",

            "berlin"

        ]


        if any(

            indicador in texto

            for indicador
            in indicadores_de

        ):

            return "DE"


        # =====================================================
        # FRANCIA
        # =====================================================

        indicadores_fr = [

            "france",

            "francia",

            "paris"

        ]


        if any(

            indicador in texto

            for indicador
            in indicadores_fr

        ):

            return "FR"


        # =====================================================
        # ITALIA
        # =====================================================

        indicadores_it = [

            "italy",

            "italia",

            "rome",

            "roma"

        ]


        if any(

            indicador in texto

            for indicador
            in indicadores_it

        ):

            return "IT"


        # =====================================================
        # JAPÓN
        # =====================================================

        indicadores_jp = [

            "japan",

            "japón",

            "japon",

            "tokyo",

            "tokio"

        ]


        if any(

            indicador in texto

            for indicador
            in indicadores_jp

        ):

            return "JP"


        # =====================================================
        # AUSTRALIA
        # =====================================================

        indicadores_au = [

            "australia",

            "sydney",

            "melbourne"

        ]


        if any(

            indicador in texto

            for indicador
            in indicadores_au

        ):

            return "AU"


        # =====================================================
        # DESCONOCIDO
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
            "united kingdom": "GB",
            "uk": "GB",
            "gb": "GB",

            "alemania": "DE",
            "germany": "DE",
            "de": "DE",

            "francia": "FR",
            "france": "FR",
            "fr": "FR",

            "italia": "IT",
            "italy": "IT",
            "it": "IT",

            "japon": "JP",
            "japón": "JP",
            "japan": "JP",
            "jp": "JP",

            "australia": "AU",
            "au": "AU"

        }


        return paises.get(

            pais_normalizado,

            pais_normalizado.upper()

        )