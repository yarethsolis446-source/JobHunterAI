from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class HomePage(QWidget):

    def __init__(self):
        super().__init__()

        self.crear_interfaz()


    def crear_interfaz(self):

        layout = QVBoxLayout(self)

        titulo = QLabel(
            "Bienvenido a JobHunter AI"
        )

        titulo.setAlignment(Qt.AlignCenter)
        titulo.setObjectName("title")


        descripcion = QLabel(
            "Tu asistente inteligente para encontrar empleo"
        )

        descripcion.setAlignment(Qt.AlignCenter)


        estado = QLabel(
            "Estado del sistema: Listo ✅"
        )

        estado.setAlignment(Qt.AlignCenter)


        layout.addStretch()

        layout.addWidget(titulo)
        layout.addWidget(descripcion)
        layout.addWidget(estado)

        layout.addStretch()