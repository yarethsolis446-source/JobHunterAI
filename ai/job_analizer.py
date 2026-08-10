from ai.job_extractor import JobExtractor



class JobAnalyzer:


    def __init__(self):

        self.extractor = JobExtractor()



    def analizar(self, empleo):


        empleo = self.extractor.extraer(
            empleo
        )


        return empleo