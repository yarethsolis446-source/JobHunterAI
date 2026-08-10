from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class ReportsPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        texto = QLabel(
            "📊 Reportes"
        )

        texto.setAlignment(Qt.AlignCenter)

        layout.addWidget(texto)