class SearchResult:


    def __init__(
        self,
        empleo,
        score,
        coincidencias,
        faltantes,
        fuente
    ):


        self.empleo = empleo

        self.score = score

        self.coincidencias = coincidencias

        self.faltantes = faltantes

        self.fuente = fuente


        # Nuevo campo

        self.nivel = ""