class Candidate:


    def __init__(
        self,
        habilidades=None,
        idiomas=None,
        profesion="",
        nivel="",
        experiencia=0,
        educacion=None
    ):


        self.habilidades = habilidades or []

        self.idiomas = idiomas or []

        self.profesion = profesion

        self.nivel = nivel

        self.experiencia = experiencia

        self.educacion = educacion or {}



    def to_dict(self):

        return {

            "profesion": self.profesion,

            "nivel": self.nivel,

            "experiencia": self.experiencia,

            "habilidades": self.habilidades,

            "idiomas": self.idiomas,

            "educacion": self.educacion

        }