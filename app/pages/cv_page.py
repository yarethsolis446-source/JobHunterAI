from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QTextEdit,
    QFileDialog,
    QMessageBox
)

from PySide6.QtCore import Qt

import os



class CVPage(QWidget):


    def __init__(self, servicio):

        super().__init__()


        self.servicio = servicio


        self.crear_interfaz()




    def crear_interfaz(self):


        layout = QVBoxLayout(
            self
        )


        titulo = QLabel(
            "Análisis de CV"
        )


        titulo.setAlignment(
            Qt.AlignCenter
        )


        layout.addWidget(
            titulo
        )



        self.btn_cargar = QPushButton(
            "📄 Cargar CV"
        )


        self.btn_cargar.clicked.connect(
            self.cargar_cv
        )


        layout.addWidget(
            self.btn_cargar
        )



        self.resultado = QTextEdit()


        self.resultado.setReadOnly(
            True
        )


        layout.addWidget(
            self.resultado
        )




    def cargar_cv(self):


        archivo, _ = QFileDialog.getOpenFileName(

            self,

            "Seleccionar CV",

            "",

            "Archivos PDF (*.pdf);;Archivos Word (*.docx)"

        )



        if not archivo:

            return



        try:


            texto = self.leer_archivo(
                archivo
            )



            perfil = self.servicio.analizar_cv(
                texto
            )



            self.mostrar_perfil(
                perfil
            )



        except Exception as e:


            QMessageBox.critical(

                self,

                "Error",

                str(e)

            )






    def leer_archivo(self, archivo):


        extension = os.path.splitext(
            archivo
        )[1].lower()



        if extension == ".pdf":


            import PyPDF2


            lector = PyPDF2.PdfReader(
                archivo
            )


            texto = ""


            for pagina in lector.pages:

                texto += pagina.extract_text() or ""



            return texto




        elif extension == ".docx":


            from docx import Document


            documento = Document(
                archivo
            )


            texto = ""


            for parrafo in documento.paragraphs:

                texto += parrafo.text + "\n"



            return texto




        else:

            raise Exception(
                "Formato no soportado"
            )






    def mostrar_perfil(self, perfil):


        texto = ""


        texto += "===== PERFIL =====\n\n"


        texto += f"Nombre: {perfil.get('nombre','')}\n"


        texto += f"Email: {perfil.get('email','')}\n"


        texto += f"Profesión: {perfil.get('profesion','')}\n\n"



        texto += "Habilidades:\n"


        for skill in perfil.get(
            "habilidades",
            []
        ):

            texto += f"- {skill}\n"



        texto += "\nIdiomas:\n"


        for idioma in perfil.get(
            "idiomas",
            []
        ):

            texto += f"- {idioma}\n"



        texto += "\nEducación:\n"


        for titulo in perfil.get(
            "titulos",
            []
        ):

            texto += f"- {titulo}\n"



        self.resultado.setText(
            texto
        )