from models.job import Job
from job_sources.base_source import BaseJobSource



class MockSource(BaseJobSource):


    def buscar_empleos(self, candidato):


        return [


            Job(

                titulo="Customer Support Agent",

                empresa="Amazon",

                habilidades=[

                    "servicio al cliente",

                    "comunicación"

                ],

                idioma="inglés",

                descripcion="Atención a clientes por chat y correo.",

                ubicacion="Costa Rica",

                remoto=True,

                salario="$1000 - $1500",

                link="https://example.com/amazon",

                fuente="Mock",

                fecha="2026"

            ),



            Job(

                titulo="Customer Success Specialist",

                empresa="Microsoft",

                habilidades=[

                    "servicio al cliente",

                    "office"

                ],

                idioma="inglés",

                descripcion="Soporte y relación con clientes.",

                ubicacion="Remoto",

                remoto=True,

                salario="$1200 - $1800",

                link="https://example.com/microsoft",

                fuente="Mock",

                fecha="2026"

            ),



            Job(

                titulo="Asistente Administrativo",

                empresa="Intel",

                habilidades=[

                    "office",

                    "excel"

                ],

                idioma="",

                descripcion="Gestión administrativa y documentos.",

                ubicacion="Heredia",

                remoto=False,

                salario="$900 - $1200",

                link="https://example.com/intel",

                fuente="Mock",

                fecha="2026"

            )


        ]