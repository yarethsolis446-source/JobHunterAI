import re

from data.skills_database import SKILLS_DATABASE

from data.skill_synonyms import SKILL_SYNONYMS





class SkillExtractor:



    def extraer(
        self,
        texto
    ):


        texto = texto.lower()


        habilidades = []



        # ==========================
        # BUSQUEDA DIRECTA
        # ==========================


        for categoria, skills in SKILLS_DATABASE.items():


            for skill in skills:



                patron = (

                    r"\b"

                    +

                    re.escape(skill)

                    +

                    r"\b"

                )



                if re.search(

                    patron,

                    texto

                ):



                    if skill not in habilidades:

                        habilidades.append(

                            skill

                        )




        # ==========================
        # SINONIMOS
        # ==========================


        for skill, sinonimos in SKILL_SYNONYMS.items():


            for sinonimo in sinonimos:



                if sinonimo.lower() in texto:



                    if skill not in habilidades:


                        habilidades.append(

                            skill

                        )



        return habilidades