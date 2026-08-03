from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame
)

from PySide6.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("JobHunter AI")
        self.resize(1200, 750)

        self.crear_interfaz()


    def crear_interfaz(self):

        principal = QWidget()
        self.setCentralWidget(principal)

        layout_principal = QHBoxLayout(principal)


        # -----------------
        # Barra lateral
        # -----------------

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(250)

        layout_sidebar = QVBoxLayout(sidebar)


        titulo = QLabel("JobHunter AI")
        titulo.setObjectName("title")

        layout_sidebar.addWidget(titulo)


        botones = [
            "🏠 Inicio",
            "📄 Mi CV",
            "🔍 Buscar empleos",
            "📊 Reportes",
            "⚙ Configuración"
        ]


        for texto in botones:

            boton = QPushButton(texto)

            layout_sidebar.addWidget(boton)


        layout_sidebar.addStretch()


        # -----------------
        # Contenido
        # -----------------

        contenido = QWidget()

        layout_contenido = QVBoxLayout(contenido)


        bienvenida = QLabel(
            "Bienvenido a JobHunter AI"
        )

        bienvenida.setAlignment(
            Qt.AlignCenter
        )

        bienvenida.setObjectName("title")


        descripcion = QLabel(
            "Tu asistente inteligente para encontrar empleo"
        )

        descripcion.setAlignment(
            Qt.AlignCenter
        )


        boton_cv = QPushButton(
            "📄 Cargar CV"
        )

        boton_buscar = QPushButton(
            "🔍 Buscar ofertas"
        )


        layout_contenido.addStretch()

        layout_contenido.addWidget(
            bienvenida
        )

        layout_contenido.addWidget(
            descripcion
        )

        layout_contenido.addWidget(
            boton_cv
        )

        layout_contenido.addWidget(
            boton_buscar
        )

        layout_contenido.addStretch()


        layout_principal.addWidget(
            sidebar
        )

        layout_principal.addWidget(
            contenido
        )