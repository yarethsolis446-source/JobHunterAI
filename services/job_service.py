from job_sources.aggregator import JobAggregator
from job_sources.test_data_sources import TestDataSource
from job_sources.jsearch_source import JSearchSource



class JobService:


    def __init__(
        self,
        api_key=None
    ):


        self.aggregator = JobAggregator()



        self.aggregator.agregar_fuente(
            TestDataSource()
        )



        if api_key:


            self.aggregator.agregar_fuente(
                JSearchSource(api_key)
            )





    def buscar_empleos(
        self,
        consulta
    ):


        return self.aggregator.obtener_empleos(
            consulta
        )