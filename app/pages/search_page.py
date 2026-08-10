from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QTextEdit,
    QScrollArea,
    QFrame
)

from PySide6.QtCore import Qt




class SearchPage(QWidget):


    def __init__(self, servicio):

        super().__init__()


        self.servicio = servicio


        self.crear_interfaz()





    def crear_interfaz(self):


        layout = QVBoxLayout(
            self
        )



        titulo = QLabel(
            "🔍 Buscar empleos"
        )

        titulo.setStyleSheet(
            "font-size:24px;font-weight:bold;"
        )



        layout.addWidget(
            titulo
        )




        self.boton_buscar = QPushButton(
            "Buscar empleos"
        )


        self.boton_buscar.clicked.connect(
            self.buscar
        )


        layout.addWidget(
            self.boton_buscar
        )





        self.resultados = QTextEdit()


        self.resultados.setReadOnly(
            True
        )


        layout.addWidget(
            self.resultados
        )







    def buscar(self):


        self.resultados.clear()


        try:


            empleos = self.servicio.buscar_empleos()



            recomendados = self.servicio.recomendar_empleos()



            if not recomendados:


                self.resultados.setText(
                    "No se encontraron empleos"
                )

                return






            texto = ""


            for empleo in recomendados[:10]:


                texto += (
                    "-------------------------\n"
                )


                texto += (
                    f"Titulo: {empleo.titulo}\n"
                )


                texto += (
                    f"Empresa: {empleo.empresa}\n"
                )


                texto += (
                    f"Compatibilidad: {empleo.score}%\n"
                )


                texto += (
                    f"Nivel: {empleo.nivel}\n"
                )


                texto += (
                    f"Coincidencias: {empleo.coincidencias}\n"
                )


                texto += (
                    f"Faltantes: {empleo.faltantes}\n"
                )


                texto += (
                    f"Link: {empleo.link}\n\n"
                )



            self.resultados.setText(
                texto
            )





        except Exception as e:


            self.resultados.setText(

                "Error:\n" + str(e)

            )