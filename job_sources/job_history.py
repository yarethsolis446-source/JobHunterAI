import json
from pathlib import Path


class JobHistory:

    def __init__(
        self,
        archivo="data/job_history.json"
    ):

        self.archivo = Path(
            archivo
        )

        # =================================================
        # CREAR CARPETA
        # =================================================

        self.archivo.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # =================================================
        # CREAR ARCHIVO SI NO EXISTE
        # =================================================

        if not self.archivo.exists():

            self.archivo.write_text(
                "[]",
                encoding="utf-8"
            )


    # =====================================================
    # CARGAR HISTORIAL
    # =====================================================

    def cargar(self):

        try:

            contenido = self.archivo.read_text(
                encoding="utf-8"
            )


            if not contenido.strip():

                return []


            datos = json.loads(
                contenido
            )


            if not isinstance(
                datos,
                list
            ):

                return []


            return datos


        except Exception:

            return []


    # =====================================================
    # GUARDAR HISTORIAL
    # =====================================================

    def guardar(
        self,
        empleos
    ):

        self.archivo.write_text(

            json.dumps(
                empleos,
                ensure_ascii=False,
                indent=4
            ),

            encoding="utf-8"
        )


    # =====================================================
    # AGREGAR EMPLEO
    # =====================================================

    def add(
        self,
        empleo
    ):

        print()
        print("==============================")
        print("GUARDANDO HISTORIAL")
        print("==============================")


        # =================================================
        # ASEGURAR DICCIONARIO
        # =================================================

        if not isinstance(
            empleo,
            dict
        ):

            raise TypeError(
                "JobHistory.add() esperaba "
                "un diccionario."
            )


        # =================================================
        # CARGAR
        # =================================================

        historial = self.cargar()


        # =================================================
        # ID
        # =================================================

        job_id = empleo.get(
            "job_id",
            ""
        )


        # =================================================
        # SI NO TIENE ID
        # =================================================

        if not job_id:

            # Usamos una combinación como respaldo.

            job_id = (
                empleo.get(
                    "titulo",
                    ""
                )
                + "_"
                +
                empleo.get(
                    "empresa",
                    ""
                )
            )


        # =================================================
        # COMPROBAR DUPLICADO
        # =================================================

        for existente in historial:

            if not isinstance(
                existente,
                dict
            ):

                continue


            existente_id = existente.get(
                "job_id",
                ""
            )


            # -------------------------------------------------
            # Comparar IDs
            # -------------------------------------------------

            if (
                existente_id
                and
                existente_id == job_id
            ):

                return False


        # =================================================
        # ASEGURAR ID
        # =================================================

        empleo["job_id"] = job_id


        # =================================================
        # AGREGAR
        # =================================================

        historial.append(
            empleo
        )


        # =================================================
        # GUARDAR
        # =================================================

        self.guardar(
            historial
        )


        return True


    # =====================================================
    # OBTENER TODO
    # =====================================================

    def obtener_todos(self):

        return self.cargar()


    # =====================================================
    # BUSCAR POR ID
    # =====================================================

    def buscar_por_id(
        self,
        job_id
    ):

        historial = self.cargar()


        for empleo in historial:

            if not isinstance(
                empleo,
                dict
            ):

                continue


            if empleo.get(
                "job_id"
            ) == job_id:

                return empleo


        return None


    # =====================================================
    # ELIMINAR
    # =====================================================

    def eliminar(
        self,
        job_id
    ):

        historial = self.cargar()


        nuevo_historial = [

            empleo

            for empleo in historial

            if (
                isinstance(
                    empleo,
                    dict
                )
                and
                empleo.get(
                    "job_id"
                ) != job_id
            )
        ]


        if len(
            nuevo_historial
        ) == len(
            historial
        ):

            return False


        self.guardar(
            nuevo_historial
        )


        return True


    # =====================================================
    # LIMPIAR
    # =====================================================

    def limpiar(self):

        self.guardar(
            []
        )