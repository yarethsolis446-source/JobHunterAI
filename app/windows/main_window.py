from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QStackedWidget
)

from app.pages.home_page import HomePage
from app.pages.cv_page import CVPage
from app.pages.search_page import SearchPage
from app.pages.reports_page import ReportsPage



class MainWindow(QMainWindow):


    def __init__(self, servicio):

        super().__init__()


        self.servicio = servicio


        self.setWindowTitle(
            "JobHunter AI"
        )


        self.resize(
            1200,
            750
        )


        self.crear_interfaz()




    def crear_interfaz(self):


        principal = QWidget()


        self.setCentralWidget(
            principal
        )


        layout_principal = QHBoxLayout(
            principal
        )



        # ==========================
        # SIDEBAR
        # ==========================


        sidebar = QFrame()


        sidebar.setObjectName(
            "sidebar"
        )


        sidebar.setFixedWidth(
            250
        )


        layout_sidebar = QVBoxLayout(
            sidebar
        )



        titulo = QLabel(
            "JobHunter AI"
        )


        titulo.setObjectName(
            "title"
        )


        layout_sidebar.addWidget(
            titulo
        )



        self.btn_inicio = QPushButton(
            "🏠 Inicio"
        )


        self.btn_cv = QPushButton(
            "📄 Mi CV"
        )


        self.btn_buscar = QPushButton(
            "🔍 Buscar empleos"
        )


        self.btn_reportes = QPushButton(
            "📊 Reportes"
        )



        layout_sidebar.addWidget(
            self.btn_inicio
        )


        layout_sidebar.addWidget(
            self.btn_cv
        )


        layout_sidebar.addWidget(
            self.btn_buscar
        )


        layout_sidebar.addWidget(
            self.btn_reportes
        )



        layout_sidebar.addStretch()




        # ==========================
        # PAGINAS
        # ==========================


        self.paginas = QStackedWidget()



        self.home_page = HomePage()



        self.cv_page = CVPage(
            self.servicio
        )



        self.search_page = SearchPage(
            self.servicio
        )



        self.reports_page = ReportsPage()




        self.paginas.addWidget(
            self.home_page
        )


        self.paginas.addWidget(
            self.cv_page
        )


        self.paginas.addWidget(
            self.search_page
        )


        self.paginas.addWidget(
            self.reports_page
        )





        # ==========================
        # NAVEGACION
        # ==========================


        self.btn_inicio.clicked.connect(

            lambda:
            self.paginas.setCurrentWidget(
                self.home_page
            )

        )



        self.btn_cv.clicked.connect(

            lambda:
            self.paginas.setCurrentWidget(
                self.cv_page
            )

        )



        self.btn_buscar.clicked.connect(

            lambda:
            self.paginas.setCurrentWidget(
                self.search_page
            )

        )



        self.btn_reportes.clicked.connect(

            lambda:
            self.paginas.setCurrentWidget(
                self.reports_page
            )

        )





        # ==========================
        # ARMAR VENTANA
        # ==========================


        layout_principal.addWidget(
            sidebar
        )


        layout_principal.addWidget(
            self.paginas
        )