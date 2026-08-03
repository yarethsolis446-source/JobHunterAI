import sys

from PySide6.QtWidgets import QApplication

from app.windows.main_window import MainWindow
from app.styles.theme import MAIN_STYLE


def main():

    app = QApplication(sys.argv)

    app.setStyleSheet(MAIN_STYLE)

    ventana = MainWindow()

    ventana.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()