
class Job:

    def __init__(
        self,
        titulo,
        empresa,
        descripcion,
        habilidades=None,
        link=None,
        ubicacion=None,
        salario=None,
        idioma="",
        experiencia=0,
        nivel="No especificado",
        job_id=None,
        remoto=False,
        pais="",
        tipo_empleo=""
    ):

        # ==========================
        # IDENTIFICADOR
        # ==========================

        self.job_id = job_id or ""

        # ==========================
        # INFORMACIÓN PRINCIPAL
        # ==========================

        self.titulo = titulo or ""
        self.empresa = empresa or ""
        self.descripcion = descripcion or ""

        # ==========================
        # DATOS DEL EMPLEO
        # ==========================

        self.habilidades = habilidades or []
        self.link = link or ""
        self.ubicacion = ubicacion or ""
        self.salario = salario or ""
        self.idioma = idioma or ""

        # ==========================
        # DATOS DEL PUESTO
        # ==========================

        self.experiencia = experiencia or 0
        self.nivel = nivel or "No especificado"

        # ==========================
        # UBICACIÓN / MODALIDAD
        # ==========================

        self.remoto = bool(remoto)
        self.pais = str(pais or "").strip().upper()
        self.tipo_empleo = tipo_empleo or ""

        # ==========================
        # RESULTADOS DEL MATCH
        # ==========================

        self.score = 0
        self.coincidencias = []
        self.faltantes = []
        self.explicacion = []

        self.modalidad = ""

    # =====================================================
    # MOSTRAR
    # =====================================================

    def mostrar(self):

        print("======================")

        print("ID:", self.job_id)
        print("Puesto:", self.titulo)
        print("Empresa:", self.empresa)
        print("País:", self.pais)
        print("Ubicación:", self.ubicacion)
        print("Remoto:", self.remoto)
        print("Tipo de empleo:", self.tipo_empleo)
        print("Nivel:", self.nivel)
        print("Experiencia:", self.experiencia, "años")
        print("Habilidades:", self.habilidades)
        print("Score:", self.score)
        print("Coincidencias:", self.coincidencias)
        print("Faltantes:", self.faltantes)
        print("Link:", self.link)

        print("======================")

