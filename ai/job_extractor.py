from data.skills_database import SKILLS_DATABASE
import re



class JobExtractor:



    def extraer(self, empleo):


        texto = ""



        if empleo.titulo:

            texto += empleo.titulo + " "



        if empleo.descripcion:

            texto += empleo.descripcion + " "



        texto = texto.lower()



        habilidades = []



        categorias = {}



        # ==========================
        # DETECTAR HABILIDADES
        # ==========================


        for categoria, skills in SKILLS_DATABASE.items():


            categorias[categoria] = []



            for skill in skills:


                if skill.lower() in texto:


                    if skill not in habilidades:

                        habilidades.append(
                            skill
                        )


                    categorias[categoria].append(
                        skill
                    )




        # ==========================
        # NIVEL DEL EMPLEO
        # ==========================


        nivel = "No especificado"



        niveles = {


            "intern": "Intern",

            "internship": "Intern",


            "junior": "Junior",

            "entry": "Junior",

            "associate": "Junior",


            "mid": "Mid",

            "intermediate": "Mid",


            "senior": "Senior",

            "lead": "Senior",

            "principal": "Senior"

        }



        for palabra, valor in niveles.items():


            if palabra in texto:


                nivel = valor

                break





        # ==========================
        # EXPERIENCIA
        # ==========================


        experiencia = 0



        patrones = [


            r"(\d+)\+?\s+years",

            r"(\d+)\+?\s+años"


        ]



        for patron in patrones:


            resultado = re.search(
                patron,
                texto
            )


            if resultado:


                experiencia = int(
                    resultado.group(1)
                )

                break





        # ==========================
        # GUARDAR RESULTADOS
        # ==========================


        empleo.habilidades = habilidades


        empleo.nivel = nivel


        empleo.experiencia = experiencia


        empleo.categorias = categorias



        return empleo