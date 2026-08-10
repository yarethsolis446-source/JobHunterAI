import re

from ai.extractors.skills_extractor import SkillExtractor
from models.candidate import Candidate


class CVAnalyzer:

    def __init__(self):

        self.skills_extractor = SkillExtractor()

    def analizar(
        self,
        texto
    ):

        texto = texto.lower()

        habilidades = self.skills_extractor.extraer(
            texto
        )

        candidato = Candidate(

            profesion=self.detectar_profesion(
                texto
            ),

            nivel=self.detectar_nivel(
                texto
            ),

            experiencia=self.detectar_experiencia(
                texto
            ),

            habilidades=habilidades,

            idiomas=self.extraer_idiomas(
                texto
            ),

            educacion=self.extraer_educacion(
                texto
            )

        )

        return candidato

    # ==========================
    # PROFESIÓN
    # ==========================

    def detectar_profesion(
        self,
        texto
    ):

        profesiones = {

            "Servicio al Cliente": [

                "servicio al cliente",
                "customer service",
                "call center",
                "agente",
                "atención al cliente",
                "chat",
                "recepción",
                "recepcion"

            ],

            "Administración": [

                "administración",
                "administracion",
                "administrativo",
                "administrativa",
                "office"

            ],

            "Programación": [

                "python",
                "flutter",
                "developer",
                "desarrollador",
                "programador",
                "software"

            ],

            "Ventas": [

                "ventas",
                "sales"

            ]

        }

        for profesion, palabras in profesiones.items():

            for palabra in palabras:

                if palabra in texto:

                    return profesion

        return "No especificada"

    # ==========================
    # NIVEL
    # ==========================

    def detectar_nivel(
        self,
        texto
    ):

        if "senior" in texto:
            return "Senior"

        if "junior" in texto:
            return "Junior"

        return "Mid"

    # ==========================
    # EXPERIENCIA
    # ==========================

    def detectar_experiencia(
        self,
        texto
    ):

        # Caso 1:
        # "3 años"

        coincidencia = re.search(
            r"(\d+(?:\.\d+)?)\s*años",
            texto
        )

        if coincidencia:

            return float(
                coincidencia.group(1)
            )

        # Caso 2:
        # Detectar años mencionados

        años = re.findall(
            r"20\d{2}",
            texto
        )

        años = sorted(
            set(
                int(a)
                for a in años
            )
        )

        if len(años) >= 2:

            experiencia = años[-1] - años[0]

            if experiencia < 0:
                experiencia = 0

            return experiencia

        return 0

    # ==========================
    # IDIOMAS
    # ==========================

    def extraer_idiomas(
        self,
        texto
    ):

        idiomas = []

        lista = {

            "inglés": [
                "inglés",
                "ingles",
                "english"
            ],

            "francés": [
                "francés",
                "frances",
                "french"
            ],

            "portugués": [
                "portugués",
                "portugues",
                "portuguese"
            ]

        }

        for idioma, palabras in lista.items():

            for palabra in palabras:

                if palabra in texto:

                    idiomas.append(
                        idioma
                    )

                    break

        return idiomas

    # ==========================
    # EDUCACIÓN
    # ==========================

    def extraer_educacion(
        self,
        texto
    ):

        educacion = {}

        if "universidad" in texto:

            educacion["universidad"] = True

        if "instituto" in texto:

            educacion["instituto"] = True

        if "ina" in texto:

            educacion["ina"] = True

        if "bachiller" in texto:

            educacion["bachiller"] = True

        if "técnico" in texto or "tecnico" in texto:

            educacion["tecnico"] = True

        return educacion