import re


class CVParser:


    def analizar(self, bloques):

        perfil = {

            "nombre": "",
            "correo": "",
            "telefono": "",
            "habilidades": [],
            "idiomas": [],
            "experiencia": "",
            "educacion": ""

        }


        texto = "\n".join(bloques)



        # ==========================
        # NOMBRE
        # ==========================

        if bloques:

            nombre = bloques[0]

            nombre = re.sub(
                r'\(.*?\)',
                '',
                nombre
            )

            nombre = re.sub(
                r'\d+.*',
                '',
                nombre
            )

            perfil["nombre"] = nombre.strip()



        # ==========================
        # CORREO
        # ==========================

        correo = re.search(
            r'[\w\.-]+@[\w\.-]+',
            texto
        )

        if correo:

            perfil["correo"] = correo.group()



        # ==========================
        # TELEFONO
        # ==========================

        telefono = re.search(
            r'\d{4}\s?\d{4}',
            texto
        )

        if telefono:

            perfil["telefono"] = telefono.group()



        # ==========================
        # EXPERIENCIA
        # ==========================

        experiencia = []

        inicio_experiencia = False


        empresas = [

            "DIGITYS",
            "VALOR GLOBAL",
            "CAFÉ BRITT",
            "CAFE BRITT"

        ]


        for bloque in bloques:


            bloque_upper = bloque.upper()



            if any(
                empresa in bloque_upper
                for empresa in empresas
            ):

                inicio_experiencia = True



            if inicio_experiencia:


                if "REFERENCIAS" in bloque_upper:

                    break



                # Evitar educación

                if (
                    "TÉCNICO EN" in bloque_upper
                    or
                    "CERTIFICACIÓN" in bloque_upper
                    or
                    "INSTITUTO NACIONAL" in bloque_upper
                ):

                    continue



                experiencia.append(
                    bloque
                )



        perfil["experiencia"] = "\n".join(
            experiencia
        )



        # ==========================
        # EDUCACION
        # ==========================

        educacion = []


        palabras_educacion = [

            "TÉCNICO EN",
            "CERTIFICACIÓN EN",
            "INSTITUTO NACIONAL",
            "APRENDIZAJE |",
            "CERTIFICACIÓN EN TECNOLOGÍA"

        ]



        for bloque in bloques:


            bloque_upper = bloque.upper()



            # Evitar títulos que no son educación

            if (
                "PERFIL" in bloque_upper
                or
                "HABILIDADES" in bloque_upper
                or
                "IDIOMAS" in bloque_upper
                or
                "REFERENCIAS" in bloque_upper
            ):

                continue



            if any(
                palabra in bloque_upper
                for palabra in palabras_educacion
            ):

                educacion.append(
                    bloque
                )



        perfil["educacion"] = "\n".join(
            educacion
        )



        # ==========================
        # HABILIDADES
        # ==========================

        habilidades = [

            "Office",
            "Excel",
            "Word",
            "Inglés",
            "Servicio al cliente",
            "Comunicación",
            "Liderazgo",
            "Resolución de conflictos",
            "Adaptabilidad",
            "Inteligencia emocional"

        ]



        for habilidad in habilidades:


            if habilidad.lower() in texto.lower():


                perfil["habilidades"].append(
                    habilidad
                )



        # ==========================
        # IDIOMAS
        # ==========================

        if "inglés" in texto.lower():

            perfil["idiomas"].append(
                "Inglés"
            )



        return perfil