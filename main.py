import sys
import os


from dotenv import load_dotenv


from PySide6.QtWidgets import QApplication


from app.windows.main_window import MainWindow


from app.styles.theme import MAIN_STYLE


from services.app_service import AppService



load_dotenv()




def main():


    api_key = os.getenv(
        "RAPIDAPI_KEY"
    )


    if api_key:

        print(
            "API Key cargada correctamente"
        )


    else:

        print(
            "No se encontró la API Key"
        )




    app = QApplication(
        sys.argv
    )



    app.setStyleSheet(
        MAIN_STYLE
    )



    servicio = AppService()



    ventana = MainWindow(
        servicio
    )



    ventana.show()



    sys.exit(
        app.exec()
    )





if __name__ == "__main__":

    main()