class SearchRequest:


    def __init__(
        self,
        puesto,
        fecha="all",
        pais="us",
        remoto=False
    ):

        self.puesto = puesto

        self.fecha = fecha

        self.pais = pais

        self.remoto = remoto