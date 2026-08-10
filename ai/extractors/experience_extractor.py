import re
from datetime import datetime


class ExperienceExtractor:


    def __init__(self):

        self.meses = {

            "enero": 1,
            "febrero": 2,
            "marzo": 3,
            "abril": 4,
            "mayo": 5,
            "junio": 6,
            "julio": 7,
            "agosto": 8,
            "septiembre": 9,
            "setiembre": 9,
            "octubre": 10,
            "noviembre": 11,
            "diciembre": 12,

            "january": 1,
            "february": 2,
            "march": 3,
            "april": 4,
            "may": 5,
            "june": 6,
            "july": 7,
            "august": 8,
            "september": 9,
            "october": 10,
            "november": 11,
            "december": 12

        }




    def extraer(self, texto):


        resultado = {


            "experiencia": 0,

            "nivel": "No especificado",

            "experiencia_detectada": False

        }



        fechas = self.extraer_fechas(
            texto
        )



        print("\n=========== EXPERIENCE EXTRACTOR ===========")



        print(
            "Fechas encontradas:"
        )



        for fecha in fechas:

            print(
                fecha.strftime("%B %Y")
            )



        meses_totales = 0




        # =====================================
        # CALCULAR PERIODOS
        # =====================================


        if len(fechas) >= 2:


            i = 0


            while i < len(fechas)-1:


                inicio = fechas[i]

                fin = fechas[i+1]



                diferencia = (

                    (fin.year - inicio.year) * 12

                    +

                    (fin.month - inicio.month)

                )



                if diferencia > 0:


                    print(

                        inicio.strftime("%B %Y"),

                        "->",

                        fin.strftime("%B %Y"),

                        "=",

                        diferencia,

                        "meses"

                    )



                    meses_totales += diferencia



                i += 2





        # =====================================
        # RESULTADOS
        # =====================================


        años = round(
            meses_totales / 12,
            1
        )



        resultado["experiencia"] = años



        if meses_totales > 0:

            resultado["experiencia_detectada"] = True



        print(
            "Total meses:",
            meses_totales
        )


        print(
            "Experiencia:",
            años
        )




        # =====================================
        # NIVEL
        # =====================================


        if meses_totales < 12:

            resultado["nivel"] = "Junior"



        elif meses_totales < 48:

            resultado["nivel"] = "Mid"



        else:

            resultado["nivel"] = "Senior"




        print(
            "Nivel:",
            resultado["nivel"]
        )



        print(
            "===========================================\n"
        )



        return resultado





    def extraer_fechas(self, texto):


        texto = texto.lower()



        fechas = []



        patron = (

            r"(enero|febrero|marzo|abril|mayo|junio|"

            r"julio|agosto|septiembre|setiembre|octubre|"

            r"noviembre|diciembre|"

            r"january|february|march|april|may|june|"

            r"july|august|september|october|november|december)"

            r"(?:\s+del?|\s+de)?"

            r"\s*"

            r"(\d{4})"

        )



        encontrados = re.findall(

            patron,

            texto

        )



        for mes, año in encontrados:



            fecha = datetime(

                int(año),

                self.meses[mes],

                1

            )



            fechas.append(
                fecha
            )



        return fechas