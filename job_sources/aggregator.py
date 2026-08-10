from models.job import Job


class JobAggregator:

    def __init__(self):

        self.sources = []


    # =====================================================
    # AGREGAR FUENTE
    # =====================================================

    def agregar_fuente(
        self,
        source
    ):

        self.sources.append(
            source
        )


    # =====================================================
    # CONVERTIR DICCIONARIO A JOB
    # =====================================================

    def convertir_a_job(
        self,
        empleo
    ):

        if isinstance(
            empleo,
            Job
        ):

            return empleo


        if isinstance(
            empleo,
            dict
        ):

            job = Job(

                titulo=empleo.get(
                    "titulo",
                    empleo.get(
                        "job_title",
                        ""
                    )
                ),

                empresa=empleo.get(
                    "empresa",
                    empleo.get(
                        "employer_name",
                        ""
                    )
                ),

                descripcion=empleo.get(
                    "descripcion",
                    empleo.get(
                        "job_description",
                        ""
                    )
                ),

                habilidades=empleo.get(
                    "habilidades",
                    empleo.get(
                        "skills",
                        []
                    )
                ),

                link=empleo.get(
                    "link",
                    empleo.get(
                        "job_apply_link",
                        ""
                    )
                ),

                ubicacion=empleo.get(
                    "ubicacion",
                    empleo.get(
                        "job_location",
                        ""
                    )
                ),

                salario=empleo.get(
                    "salario",
                    ""
                ),

                idioma=empleo.get(
                    "idioma",
                    ""
                ),

                experiencia=empleo.get(
                    "experiencia",
                    0
                ),

                nivel=empleo.get(
                    "nivel",
                    "No especificado"
                ),

                job_id=empleo.get(
                    "job_id",
                    ""
                ),

                remoto=empleo.get(
                    "remoto",
                    empleo.get(
                        "job_is_remote",
                        False
                    )
                ),

                pais=self.normalizar_pais(
                    empleo.get(
                        "pais",
                        empleo.get(
                            "job_country",
                            ""
                        )
                    )
                ),

                tipo_empleo=empleo.get(
                    "tipo_empleo",
                    empleo.get(
                        "job_employment_type",
                        ""
                    )
                )
            )


            return job


        raise TypeError(
            "Tipo de empleo no compatible: "
            f"{type(empleo)}"
        )


    # =====================================================
    # NORMALIZAR PAÍS
    # =====================================================

    def normalizar_pais(
        self,
        pais
    ):

        if not pais:

            return ""


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


    # =====================================================
    # OBTENER EMPLEOS
    # =====================================================

    def obtener_empleos(
        self,
        consulta=None,
        pais=None,
        remoto=False
    ):

        empleos = []


        print()
        print("==============================")
        print("AGREGADOR DE EMPLEOS")
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
        # NORMALIZAR PAÍS
        # =================================================

        pais_codigo = self.normalizar_pais(
            pais
        )


        print(
            "Código país:",
            pais_codigo if pais_codigo else "TODOS"
        )


        # =================================================
        # CONSULTAR TODAS LAS FUENTES
        # =================================================

        for source in self.sources:

            try:

                print()
                print(
                    "Consultando:",
                    source.__class__.__name__
                )


                resultado = source.buscar_empleos(

                    consulta,

                    pais=pais,

                    remoto=remoto

                )


                if not resultado:

                    print(
                        "La fuente no devolvió empleos."
                    )

                    continue


                # =================================================
                # CONVERTIR
                # =================================================

                for empleo in resultado:

                    try:

                        empleo_job = (
                            self.convertir_a_job(
                                empleo
                            )
                        )


                        # =========================================
                        # FILTRO DE PAÍS
                        # =========================================

                        if pais_codigo:

                            pais_empleo = (
                                self.normalizar_pais(
                                    getattr(
                                        empleo_job,
                                        "pais",
                                        ""
                                    )
                                )
                            )


                            if pais_empleo != pais_codigo:

                                print(
                                    "Descartado por país:",
                                    empleo_job.titulo,
                                    "|",
                                    pais_empleo,
                                    "!=",
                                    pais_codigo
                                )

                                continue


                        # =========================================
                        # FILTRO REMOTO
                        # =========================================

                        if remoto:

                            es_remoto = bool(
                                getattr(
                                    empleo_job,
                                    "remoto",
                                    False
                                )
                            )


                            if not es_remoto:

                                print(
                                    "Descartado por remoto:",
                                    empleo_job.titulo
                                )

                                continue


                        # =========================================
                        # AGREGAR
                        # =========================================

                        empleos.append(
                            empleo_job
                        )


                    except Exception as error:

                        print()
                        print(
                            "ERROR CONVIRTIENDO EMPLEO:"
                        )

                        print(error)


            except Exception as error:

                print()
                print(
                    "ERROR EN FUENTE:"
                )

                print(error)


        # =================================================
        # TOTAL
        # =================================================

        print()
        print("==============================")


        print(
            "TOTAL OBTENIDOS:",
            len(empleos)
        )


        print(
            "=============================="
        )


        # =================================================
        # DUPLICADOS
        # =================================================

        resultado_final = (
            self.eliminar_duplicados(
                empleos
            )
        )


        print()
        print(
            "TOTAL DESPUÉS DE DUPLICADOS:",
            len(resultado_final)
        )


        # =================================================
        # RESUMEN
        # =================================================

        print()
        print("==============================")
        print("RESULTADO FINAL")
        print("==============================")


        for empleo in resultado_final:

            print(
                "-",
                empleo.titulo,
                "|",
                empleo.pais,
                "| remoto:",
                empleo.remoto
            )


        return resultado_final


    # =====================================================
    # ELIMINAR DUPLICADOS
    # =====================================================

    def eliminar_duplicados(
        self,
        empleos
    ):

        vistos = set()

        resultado = []


        for empleo in empleos:

            if not isinstance(
                empleo,
                Job
            ):

                try:

                    empleo = (
                        self.convertir_a_job(
                            empleo
                        )
                    )

                except Exception as error:

                    print(
                        "ERROR CONVIRTIENDO EMPLEO:",
                        error
                    )

                    continue


            titulo = (
                empleo.titulo
                or ""
            )


            empresa = (
                empleo.empresa
                or ""
            )


            job_id = (
                getattr(
                    empleo,
                    "job_id",
                    ""
                )
                or ""
            )


            if job_id:

                clave = (

                    "id",

                    str(
                        job_id
                    ).strip().lower()

                )

            else:

                clave = (

                    "datos",

                    titulo.strip().lower(),

                    empresa.strip().lower()

                )


            if clave not in vistos:

                vistos.add(
                    clave
                )

                resultado.append(
                    empleo
                )


        return resultado