class LanguageExtractor:


    def extraer(self, texto):

        texto_lower = texto.lower()


        idiomas_detectados = []


        idiomas = {

            "inglés": [
                "inglés",
                "ingles",
                "english",
                "en"
            ],

            "español": [
                "español",
                "espanol",
                "spanish"
            ],

            "francés": [
                "francés",
                "frances",
                "french"
            ],

            "alemán": [
                "alemán",
                "aleman",
                "german"
            ],

            "portugués": [
                "portugués",
                "portugues",
                "portuguese"
            ],

            "italiano": [
                "italiano",
                "italian"
            ]

        }



        for idioma, palabras in idiomas.items():

            for palabra in palabras:

                if palabra in texto_lower:

                    if idioma not in idiomas_detectados:

                        idiomas_detectados.append(
                            idioma
                        )

                    break



        niveles = {

            "nativo": "Nativo",
            "native": "Nativo",

            "fluido": "Fluido",
            "fluente": "Fluido",
            "fluent": "Fluido",

            "avanzado": "Avanzado",
            "advanced": "Avanzado",
            "c1": "C1",
            "c2": "C2",

            "intermedio": "Intermedio",
            "intermediate": "Intermedio",
            "b1": "B1",
            "b2": "B2",

            "basico": "Básico",
            "básico": "Básico",
            "basic": "Básico",
            "a1": "A1",
            "a2": "A2"

        }


        nivel = "No especificado"


        for palabra, valor in niveles.items():

            if palabra in texto_lower:

                nivel = valor
                break



        resultado = {

            "idiomas": idiomas_detectados,

            "nivel": nivel

        }


        return resultado