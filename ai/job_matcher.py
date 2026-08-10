from models.job import Job


class JobMatcher:

    # =====================================================
    # EQUIVALENCIAS DE HABILIDADES
    # =====================================================

    EQUIVALENCIAS = {

        "customer service": [
            "servicio al cliente",
            "atención al cliente",
            "customer service",
            "customer support",
            "customer service representative",
            "customer service agent",
            "customer support agent",
        ],

        "communication": [
            "comunicación",
            "communication",
        ],

        "english": [
            "inglés",
            "ingles",
            "english",
        ],

        "office": [
            "office",
            "microsoft office",
        ],

        "excel": [
            "excel",
            "microsoft excel",
        ],

        "leadership": [
            "liderazgo",
            "leadership",
        ],

        "adaptability": [
            "adaptabilidad",
            "adaptability",
        ],

        "problem solving": [
            "resolución de problemas",
            "resolucion de problemas",
            "problem solving",
        ],

        "conflict resolution": [
            "resolución de conflictos",
            "resolucion de conflictos",
            "conflict resolution",
        ],

        "sales": [
            "ventas",
            "sales",
            "sales representative",
        ],

        "negotiation": [
            "negociación",
            "negociacion",
            "negotiation",
        ],

        "organization": [
            "organización",
            "organizacion",
            "organization",
        ],

        "analysis": [
            "análisis",
            "analisis",
            "analysis",
        ],

        "computer": [
            "computación",
            "computacion",
            "computer",
        ],

        "software": [
            "software",
        ],

        "programming": [
            "programación",
            "programacion",
            "programming",
        ],
    }

    # =====================================================
    # PROFESIONES RELACIONADAS
    # =====================================================

    PROFESIONES_RELACIONADAS = {

        "servicio al cliente": [
            "customer service",
            "customer support",
            "customer service agent",
            "customer support agent",
            "call center",
            "representante de servicio al cliente",
            "customer service representative",
            "atención al cliente",
            "receptionist",
            "recepcionista",
            "support agent",
            "client service",
            "customer care",
        ],

        "administración": [
            "administrative assistant",
            "administrative",
            "office assistant",
            "asistente administrativo",
            "secretary",
            "secretaria",
        ],

        "ventas": [
            "sales representative",
            "sales",
            "representante de ventas",
            "business development",
        ],

        "recursos humanos": [
            "human resources",
            "hr assistant",
            "hr",
            "recursos humanos",
        ],

        "marketing": [
            "marketing",
            "marketing assistant",
            "digital marketing",
        ],

        "tecnología": [
            "it support",
            "technical support",
            "software developer",
            "developer",
            "programmer",
            "technology",
        ],
    }

    # =====================================================
    # NORMALIZAR TEXTO
    # =====================================================

    @staticmethod
    def normalizar_texto(texto):

        if not texto:
            return ""

        return (
            str(texto)
            .lower()
            .strip()
        )

    # =====================================================
    # TEXTO COMPLETO DEL EMPLEO
    # =====================================================

    def texto_empleo(self, empleo):

        return (
            self.normalizar_texto(
                empleo.titulo
            )
            + " "
            + self.normalizar_texto(
                empleo.descripcion
            )
        )

    # =====================================================
    # COMPROBAR HABILIDAD
    # =====================================================

    def habilidad_coincide(
        self,
        habilidad_candidato,
        habilidad_empleo,
    ):

        candidato = self.normalizar_texto(
            habilidad_candidato
        )

        empleo = self.normalizar_texto(
            habilidad_empleo
        )

        if not candidato or not empleo:
            return False

        if candidato == empleo:
            return True

        if (
            candidato in empleo
            or empleo in candidato
        ):
            return True

        for grupo in self.EQUIVALENCIAS.values():

            grupo_normalizado = [
                self.normalizar_texto(x)
                for x in grupo
            ]

            if (
                candidato in grupo_normalizado
                and empleo in grupo_normalizado
            ):
                return True

        return False

    # =====================================================
    # COINCIDENCIA DE PROFESIÓN
    # =====================================================

    def profesion_coincide(
        self,
        candidato,
        empleo,
    ):

        profesion = self.normalizar_texto(
            candidato.profesion
        )

        titulo = self.normalizar_texto(
            empleo.titulo
        )

        descripcion = self.normalizar_texto(
            empleo.descripcion
        )

        if not profesion:
            return False

        if profesion in titulo:
            return True

        relaciones = self.PROFESIONES_RELACIONADAS.get(
            profesion,
            []
        )

        for relacionada in relaciones:

            relacionada = self.normalizar_texto(
                relacionada
            )

            if relacionada in titulo:
                return True

        # Solo buscamos la profesión en la descripción
        # si aparece como una frase razonablemente clara.
        for relacionada in relaciones:

            relacionada = self.normalizar_texto(
                relacionada
            )

            if relacionada and relacionada in descripcion:
                return True

        return False

    # =====================================================
    # NIVEL
    # =====================================================

    def nivel_score(
        self,
        candidato,
        empleo,
    ):

        nivel_candidato = self.normalizar_texto(
            candidato.nivel
        )

        nivel_empleo = self.normalizar_texto(
            empleo.nivel
        )

        if not nivel_candidato:
            return 0

        if (
            not nivel_empleo
            or nivel_empleo == "no especificado"
        ):
            # No penalizar, pero tampoco regalar
            # puntos completos.
            return 6

        if nivel_candidato == nivel_empleo:
            return 10

        compatibles = {

            "junior": [
                "junior",
                "entry level",
                "entry",
                "intern",
            ],

            "mid": [
                "mid",
                "mid level",
                "intermediate",
            ],

            "senior": [
                "senior",
                "lead",
                "manager",
            ],
        }

        for grupo in compatibles.values():

            if (
                nivel_candidato in grupo
                and nivel_empleo in grupo
            ):
                return 8

        # Un Mid puede ser considerado para Junior,
        # pero no recibe la misma puntuación.
        if (
            nivel_candidato == "mid"
            and nivel_empleo == "junior"
        ):
            return 9

        # Un Senior puede aplicar a Mid,
        # pero aquí el candidato es Mid.
        if (
            nivel_candidato == "mid"
            and nivel_empleo == "senior"
        ):
            return 3

        return 0

    # =====================================================
    # IDIOMA
    # =====================================================

    def idioma_score(
        self,
        candidato,
        empleo,
    ):

        idiomas = [
            self.normalizar_texto(x)
            for x in candidato.idiomas
        ]

        texto = self.texto_empleo(empleo)

        for idioma in idiomas:

            if not idioma:
                continue

            if idioma in texto:
                return 10

            if idioma in (
                "ingles",
                "inglés",
            ):

                if "english" in texto:
                    return 10

                if "inglés" in texto:
                    return 10

        # Si el empleo no menciona idioma,
        # no penalizamos.
        return 5

    # =====================================================
    # EXPERIENCIA
    # =====================================================

    def experiencia_score(
        self,
        candidato,
        empleo,
    ):

        try:

            experiencia_candidato = float(
                candidato.experiencia or 0
            )

        except (
            ValueError,
            TypeError,
        ):

            experiencia_candidato = 0

        try:

            experiencia_empleo = float(
                empleo.experiencia or 0
            )

        except (
            ValueError,
            TypeError,
        ):

            experiencia_empleo = 0

        if experiencia_empleo <= 0:
            return 10

        if experiencia_candidato >= experiencia_empleo:
            return 15

        diferencia = (
            experiencia_empleo
            - experiencia_candidato
        )

        if diferencia <= 0.5:
            return 12

        if diferencia <= 1:
            return 9

        if diferencia <= 2:
            return 5

        return 0

    # =====================================================
    # EDUCACIÓN
    # =====================================================

    def educacion_score(
        self,
        candidato,
    ):

        educacion = candidato.educacion

        if not educacion:
            return 0

        puntos = 0

        for valor in educacion.values():

            if valor:
                puntos += 1

        if puntos >= 3:
            return 5

        if puntos >= 1:
            return 3

        return 0

    # =====================================================
    # MODALIDAD
    # =====================================================

    def detectar_modalidad(
        self,
        empleo,
    ):

        texto = self.texto_empleo(
            empleo
        )

        remoto = [
            "remote",
            "remoto",
            "work from home",
            "working from home",
            "telework",
            "teletrabajo",
        ]

        hibrido = [
            "hybrid",
            "híbrido",
            "hibrido",
        ]

        for palabra in remoto:

            if palabra in texto:
                return "Remoto"

        for palabra in hibrido:

            if palabra in texto:
                return "Híbrido"

        return "Presencial"

    # =====================================================
    # SCORE DE MODALIDAD
    # =====================================================

    def modalidad_score(
        self,
        empleo,
    ):

        modalidad = self.detectar_modalidad(
            empleo
        )

        if modalidad == "Remoto":

            return 5

        if modalidad == "Híbrido":

            return 3

        return 0

    # =====================================================
    # UBICACIÓN
    # =====================================================

    def ubicacion_info(
        self,
        empleo,
    ):

        ubicacion = self.normalizar_texto(
            empleo.ubicacion
        )

        if not ubicacion:
            return "Ubicación no especificada"

        return ubicacion

    # =====================================================
    # ANALIZAR
    # =====================================================

    def analizar(
        self,
        candidato,
        empleo,
    ):

        coincidencias = []
        faltantes = []
        explicacion = []

        # =================================================
        # HABILIDADES
        # =================================================

        habilidades_candidato = [
            self.normalizar_texto(x)
            for x in candidato.habilidades
            if x
        ]

        habilidades_empleo = [
            self.normalizar_texto(x)
            for x in empleo.habilidades
            if x
        ]

        coincidencias_habilidades = 0

        for skill_empleo in habilidades_empleo:

            encontrada = False

            for skill_candidato in habilidades_candidato:

                if self.habilidad_coincide(
                    skill_candidato,
                    skill_empleo,
                ):

                    encontrada = True

                    if skill_empleo not in coincidencias:

                        coincidencias.append(
                            skill_empleo
                        )

                    coincidencias_habilidades += 1

                    break

            if not encontrada:

                faltantes.append(
                    skill_empleo
                )

        # =================================================
        # SCORE HABILIDADES
        # =================================================

        if habilidades_empleo:

            porcentaje = (
                coincidencias_habilidades
                / len(habilidades_empleo)
            )

            score_habilidades = (
                porcentaje * 35
            )

        else:

            # No regalamos 20 puntos.
            # Analizamos el texto del puesto.
            texto = self.texto_empleo(
                empleo
            )

            coincidencias_texto = 0

            for habilidad in habilidades_candidato:

                if habilidad in texto:

                    coincidencias_texto += 1

            if habilidades_candidato:

                porcentaje_texto = (
                    coincidencias_texto
                    / len(habilidades_candidato)
                )

                score_habilidades = (
                    porcentaje_texto * 20
                )

            else:

                score_habilidades = 0

        # =================================================
        # PROFESIÓN
        # =================================================

        profesion_match = self.profesion_coincide(
            candidato,
            empleo,
        )

        if profesion_match:

            score_profesion = 25

            explicacion.append(
                "El puesto coincide con tu área profesional"
            )

        else:

            score_profesion = 0

        # =================================================
        # EXPERIENCIA
        # =================================================

        score_experiencia = (
            self.experiencia_score(
                candidato,
                empleo,
            )
        )

        if score_experiencia >= 15:

            explicacion.append(
                "Tu experiencia cumple con lo requerido"
            )

        elif score_experiencia >= 10:

            explicacion.append(
                "Tu experiencia es cercana a la requerida"
            )

        elif empleo.experiencia > 0:

            explicacion.append(
                "El puesto requiere más experiencia"
            )

        # =================================================
        # IDIOMA
        # =================================================

        score_idioma = self.idioma_score(
            candidato,
            empleo,
        )

        if score_idioma >= 10:

            explicacion.append(
                "El puesto utiliza uno de tus idiomas"
            )

        # =================================================
        # NIVEL
        # =================================================

        score_nivel = self.nivel_score(
            candidato,
            empleo,
        )

        if score_nivel >= 9:

            explicacion.append(
                "El nivel profesional es compatible"
            )

        elif score_nivel <= 3:

            explicacion.append(
                "El nivel del puesto puede estar por encima "
                "de tu experiencia actual"
            )

        # =================================================
        # EDUCACIÓN
        # =================================================

        score_educacion = (
            self.educacion_score(
                candidato
            )
        )

        if score_educacion > 0:

            explicacion.append(
                "Tu formación académica aporta al perfil"
            )

        # =================================================
        # MODALIDAD
        # =================================================

        modalidad = self.detectar_modalidad(
            empleo
        )

        score_modalidad = (
            self.modalidad_score(
                empleo
            )
        )

        if modalidad == "Remoto":

            explicacion.append(
                "El puesto ofrece modalidad remota"
            )

        elif modalidad == "Híbrido":

            explicacion.append(
                "El puesto ofrece modalidad híbrida"
            )

        # =================================================
        # SCORE FINAL
        # =================================================

        score = (
            score_habilidades
            + score_profesion
            + score_experiencia
            + score_idioma
            + score_nivel
            + score_educacion
            + score_modalidad
        )

        score = round(
            min(score, 100)
        )

        # =================================================
        # EXPLICACIÓN DE HABILIDADES
        # =================================================

        if habilidades_empleo:

            explicacion.insert(
                0,
                f"Coincides con "
                f"{coincidencias_habilidades} de "
                f"{len(habilidades_empleo)} "
                f"habilidades requeridas",
            )

        else:

            explicacion.insert(
                0,
                "La oferta no especifica habilidades "
                "estructuradas; se analizaron el título "
                "y la descripción",
            )

        # =================================================
        # NIVEL FINAL
        # =================================================

        if score >= 85:

            nivel = "⭐ Excelente coincidencia"

        elif score >= 70:

            nivel = "🟢 Muy buena coincidencia"

        elif score >= 55:

            nivel = "🟡 Buena coincidencia"

        elif score >= 40:

            nivel = "🟠 Posible coincidencia"

        else:

            nivel = "🔴 Baja coincidencia"

        # =================================================
        # UBICACIÓN
        # =================================================

        ubicacion = self.ubicacion_info(
            empleo
        )

        # =================================================
        # SI NO HAY COINCIDENCIAS
        # =================================================

        if (
            not coincidencias
            and not profesion_match
        ):

            explicacion.append(
                "No se encontraron coincidencias "
                "directas importantes con tu perfil"
            )

        # =================================================
        # GUARDAR RESULTADOS
        # =================================================

        empleo.score = score

        empleo.coincidencias = list(
            dict.fromkeys(
                coincidencias
            )
        )

        empleo.faltantes = list(
            dict.fromkeys(
                faltantes
            )
        )

        empleo.explicacion = list(
            dict.fromkeys(
                explicacion
            )
        )

        # Guardamos modalidad si el modelo Job
        # permite atributos dinámicos.
        empleo.modalidad = modalidad

        return {

            "score": score,

            "nivel": nivel,

            "modalidad": modalidad,

            "ubicacion": ubicacion,

            "coincidencias":
                empleo.coincidencias,

            "faltantes":
                empleo.faltantes,

            "explicacion":
                empleo.explicacion,
        }
