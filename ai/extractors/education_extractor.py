class EducationExtractor:

    def extraer(self, texto):

        texto_lower = texto.lower()

        resultado = {
            "universidades": [],
            "titulos": [],
            "certificaciones": [],
            "cursos": []
        }

        # ==========================
        # UNIVERSIDADES
        # ==========================

        universidades = [

            "universidad",
            "university",
            "college",
            "instituto",
            "institute",
            "tec",
            "utn",
            "una",
            "ucr",
            "ulacit"

        ]

        for palabra in universidades:

            if palabra in texto_lower:

                resultado["universidades"].append(
                    palabra.title()
                )

        # ==========================
        # TITULOS
        # ==========================

        titulos = {

            "ingeniería": "Ingeniería",
            "ingenieria": "Ingeniería",
            "engineering": "Engineering",

            "licenciatura": "Licenciatura",
            "bachelor": "Bachelor",

            "maestría": "Maestría",
            "maestria": "Maestría",
            "master": "Master",

            "doctorado": "Doctorado",
            "phd": "PhD",

            "técnico": "Técnico",
            "tecnico": "Técnico",

            "bootcamp": "Bootcamp"

        }

        for palabra, titulo in titulos.items():

            if palabra in texto_lower:

                if titulo not in resultado["titulos"]:

                    resultado["titulos"].append(
                        titulo
                    )

        # ==========================
        # CERTIFICACIONES
        # ==========================

        certificaciones = [

            "aws",
            "azure",
            "google cloud",
            "gcp",
            "oracle",
            "cisco",
            "ccna",
            "ccnp",
            "scrum",
            "pmp",
            "comptia",
            "itil",
            "kubernetes",
            "docker"

        ]

        for cert in certificaciones:

            if cert in texto_lower:

                resultado["certificaciones"].append(
                    cert.upper()
                )

        # ==========================
        # CURSOS
        # ==========================

        palabras_curso = [

            "course",
            "curso",
            "bootcamp",
            "certification",
            "certificado"

        ]

        if any(
            palabra in texto_lower
            for palabra in palabras_curso
        ):

            resultado["cursos"].append(
                "Cursos detectados"
            )

        return resultado