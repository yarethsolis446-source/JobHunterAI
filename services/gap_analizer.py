class GapAnalyzer:

    def analizar(self, empleo):

        faltantes = empleo.faltantes

        prioridad = []

        importantes = {

            "aws": 10,
            "azure": 10,
            "docker": 9,
            "kubernetes": 9,
            "react": 8,
            ".net": 8,
            "flutter": 8,
            "sql": 8,
            "python": 9,
            "java": 8,
            "git": 7,
            "office": 4,
            "excel": 4

        }

        prioridad = sorted(

            faltantes,

            key=lambda x: importantes.get(x, 5),

            reverse=True

        )

        return prioridad