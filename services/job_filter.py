class JobFilter:

    def __init__(self, limite=500):

        self.limite = limite

    def filtrar(
        self,
        empleos,
        ubicacion=None,
        remoto=None,
        idioma=None
    ):

        resultados = []

        for empleo in empleos:

            # ==========================
            # FILTRO UBICACIÓN
            # ==========================

            if ubicacion:

                if hasattr(empleo, "ubicacion"):

                    if ubicacion.lower() not in empleo.ubicacion.lower():

                        continue

            # ==========================
            # FILTRO REMOTO
            # ==========================

            if remoto is not None:

                if hasattr(empleo, "remoto"):

                    if empleo.remoto != remoto:

                        continue

            # ==========================
            # FILTRO IDIOMA
            # ==========================

            if idioma:

                encontrado = False

                if hasattr(empleo, "idioma"):

                    if empleo.idioma:

                        if idioma.lower() in empleo.idioma.lower():

                            encontrado = True

                if not encontrado:

                    continue

            resultados.append(empleo)

            if len(resultados) >= self.limite:

                break

        return resultados

    def eliminar_duplicados(self, empleos):

        vistos = set()

        resultado = []

        for empleo in empleos:

            titulo = ""

            empresa = ""

            if hasattr(empleo, "titulo"):

                titulo = empleo.titulo.lower().strip()

            if hasattr(empleo, "empresa"):

                empresa = empleo.empresa.lower().strip()

            clave = (titulo, empresa)

            if clave not in vistos:

                vistos.add(clave)

                resultado.append(empleo)

        return resultado

    def limitar(self, empleos):

        return empleos[: self.limite]

    def contar_remotos(self, empleos):

        return len(

            [

                empleo

                for empleo in empleos

                if hasattr(empleo, "remoto")

                and empleo.remoto

            ]

        )

    def contar_presenciales(self, empleos):

        return len(

            [

                empleo

                for empleo in empleos

                if hasattr(empleo, "remoto")

                and not empleo.remoto

            ]

        )

    def obtener_empresas(self, empleos):

        empresas = set()

        for empleo in empleos:

            if hasattr(empleo, "empresa"):

                empresas.add(

                    empleo.empresa

                )

        return sorted(list(empresas))

    def estadisticas(self, empleos):

        return {

            "total": len(empleos),

            "remotos": self.contar_remotos(empleos),

            "presenciales": self.contar_presenciales(empleos),

            "empresas": len(self.obtener_empresas(empleos))

        }