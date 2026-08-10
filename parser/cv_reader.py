import fitz


class CVReader:

    @staticmethod
    def leer_pdf(ruta_pdf):

        documento = fitz.open(ruta_pdf)

        texto = ""

        for pagina in documento:

            texto += pagina.get_text()

            texto += "\n"

        documento.close()

        return texto.strip()