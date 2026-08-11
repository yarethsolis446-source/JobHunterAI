
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
        # PARAMETROS
        # =====================================================

        params = {

            "query":
                consulta or "software developer",

            "page":
                "1",

            "num_pages":
                "1",

            "date_posted":
                fecha

        }


        # =====================================================
        # PAIS
        # =====================================================

        if pais:

            codigo = self.convertir_pais(
                pais
            )

            if codigo:

                params["country"] = codigo


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
        # REQUEST
        # =====================================================

        try:

            print()
            print("========================================")
            print("ENVIANDO REQUEST A RAPIDAPI...")
            print("========================================")


            respuesta = requests.get(

                self.url,

                headers=headers,

                params=params,

                timeout=30

            )


            # =================================================
            # STATUS
            # =================================================

            print()
            print("========================================")
            print("RESPUESTA DE RAPIDAPI")
            print("========================================")

            print(
                "STATUS:",
                respuesta.status_code
            )


            print()
            print("URL FINAL:")

            print(
                respuesta.url
            )


            print()
            print("HEADERS:")

            print(
                dict(
                    respuesta.headers
                )
            )


            print()
            print("RESPUESTA RAW:")

            print(
                respuesta.text
            )


            # =================================================
            # ERROR HTTP
            # =================================================

            if respuesta.status_code != 200:

                print()
                print("========================================")
                print("❌ JSEARCH DEVOLVIÓ ERROR")
                print("========================================")

                print(
                    "STATUS:",
                    respuesta.status_code
                )

                return []


            # =================================================
            # JSON
            # =================================================

            try:

                datos = respuesta.json()

            except Exception as error:

                print()
                print("❌ ERROR CONVIRTIENDO JSON")

                print(
                    error
                )

                return []


            print()
            print("========================================")
            print("JSON DECODIFICADO")
            print("========================================")

            print(
                datos
            )


            # =================================================
            # DATA
            # =================================================

            trabajos = datos.get(
                "data",
                []
            )


            print()
            print("========================================")
            print("DATA JSEARCH")
            print("========================================")

            print(
                "Tipo:",
                type(trabajos)
            )

            print(
                "Cantidad:",
                len(trabajos)
                if isinstance(trabajos, list)
                else "NO ES LISTA"
            )


            if not isinstance(
                trabajos,
                list
            ):

                print(
                    "❌ data no es una lista"
                )

                return []


            if not trabajos:

                print()
                print(
                    "⚠️ JSEARCH RESPONDIÓ 200 "
                    "PERO NO DEVOLVIÓ EMPLEOS"
                )

                return []


            # =================================================
            # MOSTRAR EMPLEOS
            # =================================================

            print()
            print("========================================")
            print("EMPLEOS RECIBIDOS")
            print("========================================")


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


            # =================================================
            # CONVERTIR
            # =================================================

            empleos = []


            for oferta in trabajos:

                if not isinstance(
                    oferta,
                    dict
                ):

                    continue


                job_id = (
                    oferta.get(
                        "job_id"
                    )
                    or ""
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


                ubicacion_api = (
                    oferta.get(
                        "job_location"
                    )
                    or ""
                )


                # =================================================
                # PAIS
                # =================================================

                pais_final = self.detectar_pais(

                    pais_oferta,

                    ciudad,

                    estado,

                    ubicacion_api,

                    descripcion,

                    empresa

                )


                # =================================================
                # UBICACION
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


                if not partes and ubicacion_api:

                    partes.append(
                        str(
                            ubicacion_api
                        ).strip()
                    )


                ubicacion = ", ".join(
                    partes
                )


                # =================================================
                # REMOTO
                # =================================================

                remoto_oferta = self.convertir_bool(

                    oferta.get(
                        "job_is_remote",
                        False
                    )

                )


                texto_remoto = " ".join(

                    [

                        str(
                            titulo
                        ),

                        str(
                            descripcion
                        ),

                        str(
                            ubicacion_api
                        )

                    ]

                ).lower()


                indicadores = [

                    "remote",

                    "remoto",

                    "remota",

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

                    for palabra in indicadores

                ):

                    remoto_oferta = True


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
                # SALARIO
                # =================================================

                salario = ""


                minimo = oferta.get(
                    "job_min_salary"
                )


                maximo = oferta.get(
                    "job_max_salary"
                )


                periodo = (
                    oferta.get(
                        "job_salary_period"
                    )
                    or ""
                )


                if (
                    minimo is not None
                    and
                    maximo is not None
                ):

                    salario = (
                        f"{minimo} - {maximo}"
                    )


                elif minimo is not None:

                    salario = str(
                        minimo
                    )


                elif maximo is not None:

                    salario = str(
                        maximo
                    )


                if salario and periodo:

                    salario += (
                        f" / {periodo}"
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
                # TIPO
                # =================================================

                tipo_empleo = (
                    oferta.get(
                        "job_employment_type"
                    )
                    or ""
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


            # =================================================
            # FILTRO PAIS
            # =================================================

            if pais:

                pais_codigo = self.convertir_pais(
                    pais
                )


                empleos = [

                    empleo

                    for empleo
                    in empleos

                    if empleo.pais == pais_codigo

                ]


            # =================================================
            # FILTRO REMOTO
            # =================================================

            if remoto:

                empleos = [

                    empleo

                    for empleo
                    in empleos

                    if empleo.remoto

                ]


            # =================================================
            # RESULTADO
            # =================================================

            print()
            print("========================================")
            print("✅ JSEARCH FUNCIONA")
            print("========================================")

            print(
                "EMPLEOS RECIBIDOS:",
                len(empleos)
            )


            return empleos


        except requests.exceptions.Timeout:

            print()
            print("❌ TIMEOUT CON JSEARCH")

            return []


        except requests.exceptions.RequestException as error:

            print()
            print("❌ ERROR REQUEST JSEARCH:")

            print(
                repr(error)
            )

            return []


        except Exception as error:

            print()
            print("========================================")
            print("❌ ERROR INTERNO JSEARCH")
            print("========================================")

            print(
                "TIPO:",
                type(error).__name__
            )

            print(
                "ERROR:",
                str(error)
            )

            print(
                "REPR:",
                repr(error)
            )

            return []


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

        if pais:

            codigo = self.convertir_pais(
                pais
            )

            if codigo:

                return codigo


        texto = " ".join(

            [

                str(
                    pais or ""
                ),

                str(
                    ciudad or ""
                ),

                str(
                    estado or ""
                ),

                str(
                    ubicacion or ""
                ),

                str(
                    descripcion or ""
                ),

                str(
                    empresa or ""
                )

            ]

        ).lower()


        indicadores = {

            "CR": [

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

            ],

            "US": [

                "united states",
                "usa",
                "u.s.a",
                "u.s."

            ],

            "CA": [

                "canada",
                "canadá"

            ],

            "MX": [

                "mexico",
                "méxico",
                "cdmx",
                "ciudad de mexico",
                "ciudad de méxico"

            ],

            "CO": [

                "colombia",
                "bogota",
                "bogotá",
                "medellin",
                "medellín"

            ],

            "ES": [

                "españa",
                "espana",
                "madrid",
                "barcelona"

            ]

        }


        for codigo, palabras in indicadores.items():

            for palabra in palabras:

                if palabra in texto:

                    return codigo


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


        valor = (

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

            valor,

            valor.upper()

        )

