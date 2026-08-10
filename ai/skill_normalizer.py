
class SkillNormalizer:

    # =====================================================
    # EQUIVALENCIAS DE HABILIDADES
    # =====================================================

    EQUIVALENCIAS = {

        "servicio al cliente": [
            "servicio al cliente",
            "atención al cliente",
            "atencion al cliente",
            "customer service",
            "customer support",
            "soporte al cliente"
        ],

        "comunicación": [
            "comunicación",
            "comunicacion",
            "comunicación efectiva",
            "comunicacion efectiva",
            "communication"
        ],

        "office": [
            "office",
            "microsoft office",
            "ms office",
            "microsoft 365",
            "office 365"
        ],

        "excel": [
            "excel",
            "microsoft excel",
            "ms excel",
            "hojas de cálculo",
            "hojas de calculo"
        ],

        "inglés": [
            "inglés",
            "ingles",
            "english"
        ],

        "programación": [
            "programación",
            "programacion",
            "programming",
            "desarrollo de software",
            "software development"
        ],

        "python": [
            "python",
            "python programming"
        ],

        "bases de datos": [
            "bases de datos",
            "base de datos",
            "database",
            "databases",
            "sql"
        ],

        "soporte técnico": [
            "soporte técnico",
            "soporte tecnico",
            "technical support",
            "it support",
            "help desk"
        ],

        "computación": [
            "computación",
            "computacion",
            "informática",
            "informatica",
            "computer skills",
            "computer"
        ],

        "resolución de problemas": [
            "resolución de problemas",
            "resolucion de problemas",
            "problem solving",
            "solución de problemas",
            "solucion de problemas"
        ],

        "organización": [
            "organización",
            "organizacion",
            "organization",
            "organizational skills"
        ],

        "adaptabilidad": [
            "adaptabilidad",
            "adaptability",
            "flexibilidad",
            "flexibility"
        ],

        "liderazgo": [
            "liderazgo",
            "leadership",
            "lider"
        ],

        "ventas": [
            "ventas",
            "sales",
            "sales representative",
            "venta"
        ],

        "negociación": [
            "negociación",
            "negociacion",
            "negotiation"
        ],

        "marketing": [
            "marketing",
            "mercadeo",
            "mercadotecnia"
        ],

        "redes sociales": [
            "redes sociales",
            "social media",
            "social networks"
        ],

        "creatividad": [
            "creatividad",
            "creativity"
        ],

        "testing": [
            "testing",
            "pruebas de software",
            "software testing",
            "qa",
            "quality assurance"
        ],

        "análisis": [
            "análisis",
            "analisis",
            "analysis",
            "análisis de datos",
            "analisis de datos",
            "data analysis"
        ],

        "estadística": [
            "estadística",
            "estadistica",
            "statistics"
        ],

        "recursos humanos": [
            "recursos humanos",
            "human resources",
            "hr",
            "rrhh",
            "rr. hh."
        ]
    }

    # =====================================================
    # NORMALIZAR HABILIDADES
    # =====================================================

    def normalizar(self, habilidades):

        resultado = []

        # Palabras que suelen generar falsos positivos

        ignorar = [
            "ui",
            "ux",
            "go",
            "it"
        ]

        for habilidad in habilidades:

            # ---------------------------------------------
            # LIMPIAR
            # ---------------------------------------------

            habilidad = (
                habilidad
                .lower()
                .strip()
            )

            # ---------------------------------------------
            # ELIMINAR VACÍOS
            # ---------------------------------------------

            if not habilidad:
                continue

            # ---------------------------------------------
            # IGNORAR PALABRAS PROBLEMÁTICAS
            # ---------------------------------------------

            if habilidad in ignorar:
                continue

            # ---------------------------------------------
            # EVITAR PALABRAS DEMASIADO CORTAS
            # ---------------------------------------------

            if len(habilidad) <= 2:
                continue

            # ---------------------------------------------
            # BUSCAR EQUIVALENCIA
            # ---------------------------------------------

            habilidad_normalizada = habilidad

            for principal, equivalentes in (
                self.EQUIVALENCIAS.items()
            ):

                if habilidad in equivalentes:

                    habilidad_normalizada = principal

                    break

            # ---------------------------------------------
            # EVITAR DUPLICADOS
            # ---------------------------------------------

            if habilidad_normalizada not in resultado:

                resultado.append(
                    habilidad_normalizada
                )

        return resultado

