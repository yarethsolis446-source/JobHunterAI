class ProfessionExtractor:

    def __init__(self):

        self.profesiones = {

            "Software Development":[

                "software engineer",
                "software developer",
                "developer",
                "programmer",
                "backend developer",
                "backend engineer",
                "frontend developer",
                "frontend engineer",
                "full stack developer",
                "full stack engineer",
                "mobile developer",
                "android developer",
                "ios developer",
                "web developer",
                "python developer",
                "java developer",
                "flutter developer",
                "react developer",
                "devops engineer",
                "qa engineer",
                "qa analyst",
                "test engineer",
                "software architect",
                "technical lead",
                "tech lead"
            ],

            "Artificial Intelligence":[

                "machine learning engineer",
                "ai engineer",
                "artificial intelligence engineer",
                "deep learning engineer",
                "computer vision engineer",
                "nlp engineer",
                "data scientist",
                "data analyst",
                "ml engineer",
                "research scientist"
            ],

            "Cybersecurity":[

                "security analyst",
                "cybersecurity analyst",
                "security engineer",
                "penetration tester",
                "ethical hacker",
                "soc analyst",
                "security consultant"
            ],

            "Cloud":[

                "cloud engineer",
                "cloud architect",
                "aws engineer",
                "azure engineer",
                "gcp engineer",
                "site reliability engineer",
                "sre"
            ],

            "Design":[

                "ui designer",
                "ux designer",
                "ui ux designer",
                "graphic designer",
                "product designer",
                "visual designer"
            ],

            "Marketing":[

                "marketing specialist",
                "digital marketing",
                "seo specialist",
                "sem specialist",
                "content creator",
                "community manager"
            ],

            "Business":[

                "project manager",
                "product manager",
                "scrum master",
                "business analyst"
            ],

            "Healthcare":[

                "doctor",
                "physician",
                "nurse",
                "registered nurse",
                "medical assistant",
                "pharmacist"
            ],

            "Education":[

                "teacher",
                "professor",
                "lecturer",
                "tutor",
                "instructor"
            ]

        }

    def extraer(self, texto):

        texto = texto.lower()

        mejor = ""

        coincidencias = 0

        categoria = ""

        for area, lista in self.profesiones.items():

            for profesion in lista:

                if profesion in texto:

                    palabras = len(profesion.split())

                    if palabras > coincidencias:

                        coincidencias = palabras

                        mejor = profesion.title()

                        categoria = area

        return {

            "profesion": mejor,

            "categoria": categoria

        }