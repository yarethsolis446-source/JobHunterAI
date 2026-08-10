from ai.cv_analyzer import CVAnalyzer
from ai.job_analizer import JobAnalyzer
from ai.job_extractor import JobExtractor
from ai.job_matcher import JobMatcher

from services.cv_score_service import CVScoreService
from services.ranking_service import RankingService

from models.candidate import Candidate




class JobPipeline:



    def __init__(self, fuente_empleos):


        self.fuente_empleos = fuente_empleos


        self.cv_analyzer = CVAnalyzer()


        self.job_analyzer = JobAnalyzer()


        self.job_extractor = JobExtractor()


        self.cv_score = CVScoreService()


        self.matcher = JobMatcher()


        self.ranking = RankingService()






    def ejecutar(self, cv_texto, busqueda):



        # ==========================
        # ANALIZAR CV
        # ==========================


        perfil = self.cv_analyzer.analizar(
            cv_texto
        )



        print("\nDEBUG PERFIL:")

        print(perfil)




        # ==========================
        # SCORE CV
        # ==========================


        cv_evaluacion = self.cv_score.evaluar(
            perfil
        )






        # ==========================
        # CREAR CANDIDATO
        # ==========================


        candidato = Candidate(

            habilidades=perfil.get(
                "habilidades",
                []
            ),

            idiomas=perfil.get(
                "idiomas",
                []
            ),

            profesion=perfil.get(
                "profesion",
                ""
            ),

            nivel=perfil.get(
                "nivel",
                ""
            )

        )







        # ==========================
        # BUSCAR EMPLEOS
        # ==========================


        empleos_raw = self.fuente_empleos.obtener_empleos(

            consulta=busqueda.puesto,

            fecha=busqueda.fecha

        )





        resultados = []






        # ==========================
        # ANALIZAR EMPLEOS
        # ==========================


        for empleo_raw in empleos_raw:



            # Convertir datos externos a Job

            empleo = self.job_extractor.extraer(

                empleo_raw

            )



            # Analizar descripción

            empleo = self.job_analyzer.analizar(

                empleo

            )




            # Comparar candidato

            analisis = self.matcher.analizar(

                candidato,

                empleo

            )





            empleo.score = analisis["score"]


            empleo.coincidencias = analisis["coincidencias"]


            empleo.faltantes = analisis["faltantes"]


            empleo.nivel = analisis["nivel"]


            empleo.explicacion = analisis["explicacion"]







            # ==========================
            # RECOMENDACION
            # ==========================



            if empleo.score >= 85:


                empleo.recomendacion = (

                    "Aplicar inmediatamente"

                )


            elif empleo.score >= 60:


                empleo.recomendacion = (

                    "Buena oportunidad"

                )


            elif empleo.score >= 40:


                empleo.recomendacion = (

                    "Revisar requisitos faltantes"

                )


            else:


                empleo.recomendacion = (

                    "Buscar oportunidades más relacionadas"

                )





            resultados.append(

                empleo

            )







        # ==========================
        # ORDENAR
        # ==========================


        resultados = self.ranking.ordenar(

            resultados

        )







        return {


            "perfil": perfil,


            "cv_score": cv_evaluacion,


            "empleos": resultados


        }