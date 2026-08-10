class RankingService:


    def ordenar(self, empleos):


        for empleo in empleos:


            # ==========================
            # BONIFICAR BUEN MATCH
            # ==========================


            score = empleo.score



            # Penalizar muchos faltantes

            faltantes = len(
                empleo.faltantes
            )


            if faltantes >= 5:

                score -= 10


            elif faltantes >= 3:

                score -= 5



            # Bonificar coincidencias

            coincidencias = len(
                empleo.coincidencias
            )


            if coincidencias >= 5:

                score += 5


            elif coincidencias >= 3:

                score += 3



            # Evitar pasar de límites

            if score > 100:

                score = 100


            if score < 0:

                score = 0



            empleo.score = score




        # ==========================
        # ORDENAR MAYOR A MENOR
        # ==========================


        empleos.sort(

            key=lambda x: x.score,

            reverse=True

        )


        return empleos