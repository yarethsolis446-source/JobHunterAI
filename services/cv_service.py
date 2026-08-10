from parser.cv_reader import CVReader
from parser.cv_parser import CVParser
from ai.cv_analyzer import CVAnalyzer
from models.candidate import Candidate



class CVService:


    def procesar_cv(self, ruta):


        # Leer PDF

        bloques = CVReader.leer_pdf(ruta)



        # Convertir bloques a texto

        texto = "\n".join(
            bloques
        )



        # Extraer datos básicos

        parser = CVParser()

        datos = parser.analizar(
            bloques
        )



        # Analizar con IA

        analyzer = CVAnalyzer()

        perfil_ai = analyzer.analizar(
            texto
        )



        # Crear candidato

        candidato = Candidate(


            nombre=datos["nombre"],

            correo=datos["correo"],

            telefono=datos["telefono"],


            profesion=perfil_ai["profesion"],


            experiencia=datos["experiencia"],


            educacion=datos["educacion"],


            habilidades=perfil_ai["habilidades"],


            idiomas=perfil_ai["idiomas"]

        )



        return candidato