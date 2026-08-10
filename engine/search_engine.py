from services.job_service import JobService
from services.job_filter import JobFilter
from services.ranking_service  import RankingService
from ai.job_matcher import JobMatcher
from models.search_result import SearchResult



class SearchEngine:


    def __init__(self):


        self.job_service = JobService()


        self.job_filter = JobFilter(

            limite=500

        )


        self.matcher = JobMatcher()


        self.ranking = RankingService(

            limite=50

        )



    def buscar(

        self,

        candidato,

        ubicacion=None,

        remoto=None,

        idioma=None

    ):


        # Buscar todas las ofertas disponibles

        empleos = self.job_service.buscar_empleos(

            candidato

        )



        # Filtrar antes de analizar

        empleos = self.job_filter.filtrar(

            empleos,

            ubicacion=ubicacion,

            remoto=remoto,

            idioma=idioma

        )



        resultados = []



        # Analizar compatibilidad

        for empleo in empleos:


            analisis = self.matcher.analizar(

                candidato,

                empleo

            )



            resultado = SearchResult(

                empleo=empleo,

                score=analisis["score"],

                coincidencias=analisis["coincidencias"],

                faltantes=analisis["faltantes"],

                fuente=empleo.fuente

            )


            resultados.append(

                resultado

            )



        # Ranking final

        resultados = self.ranking.ordenar(

            resultados

        )



        return resultados