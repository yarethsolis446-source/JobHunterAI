class CVScoreService:


    def evaluar(self, perfil):


        score = 0


        recomendaciones = []



        # ==========================
        # INFORMACION PERSONAL
        # 15 puntos
        # ==========================


        if perfil.get("nombre"):

            score += 5


        if perfil.get("email"):

            score += 5


        if perfil.get("telefono"):

            score += 5



        if not perfil.get("email"):

            recomendaciones.append(
                "Agrega un correo electrónico."
            )


        if not perfil.get("telefono"):

            recomendaciones.append(
                "Agrega un número de teléfono."
            )




        # ==========================
        # HABILIDADES
        # 30 puntos
        # ==========================


        habilidades = perfil.get(
            "habilidades",
            []
        )


        cantidad_habilidades = len(
            habilidades
        )


        if cantidad_habilidades >= 8:

            score += 30


        elif cantidad_habilidades >= 5:

            score += 20


        elif cantidad_habilidades >= 2:

            score += 10


        else:

            recomendaciones.append(
                "Agrega más habilidades técnicas."
            )




        # ==========================
        # EXPERIENCIA
        # 25 puntos
        # ==========================


        anios = perfil.get(
            "anios",
            0
        )


        experiencia = perfil.get(
            "experiencia_detectada",
            False
        )



        if anios >= 5:

            score += 25



        elif anios >= 2:

            score += 20



        elif experiencia:

            score += 10



        else:

            recomendaciones.append(
                "Agrega experiencia laboral o proyectos realizados."
            )




        # ==========================
        # EDUCACION
        # 15 puntos
        # ==========================


        titulos = perfil.get(
            "titulos",
            []
        )


        universidades = perfil.get(
            "universidades",
            []
        )



        if titulos and universidades:

            score += 15


        elif titulos:

            score += 10


        else:

            recomendaciones.append(
                "Agrega estudios o títulos académicos."
            )




        # ==========================
        # IDIOMAS
        # 15 puntos
        # ==========================


        idiomas = perfil.get(
            "idiomas",
            []
        )


        nivel = perfil.get(
            "nivel_idioma",
            ""
        )



        if idiomas:


            score += 10



            if nivel in [

                "Nativo",
                "Fluido",
                "C1",
                "C2"

            ]:

                score += 5


        else:

            recomendaciones.append(
                "Agrega idiomas."
            )




        # ==========================
        # LIMITE DE SCORE
        # ==========================


        if score > 100:

            score = 100



        if score < 0:

            score = 0




        # ==========================
        # RESULTADO
        # ==========================


        return {


            # Compatible con código anterior

            "score": score,


            # Nuevo nombre más claro

            "puntaje": score,


            "recomendaciones": recomendaciones


        }