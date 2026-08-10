from models.job import Job
from ai.job_matcher import JobMatcher
from models.candidate import Candidate



# Crear candidato de prueba

candidato = Candidate(

    nombre="Beatriz Brenes Arce",

    profesion="Atención al cliente",

    habilidades=[
        "Office",
        "liderazgo",
        "comunicación",
        "servicio al cliente"
    ],

    idiomas=[
        "Inglés"
    ]

)



# Crear empleos de prueba

empleos = [

    Job(
        titulo="Customer Support Agent",
        empresa="Empresa A",
        habilidades=[
            "servicio al cliente",
            "comunicación",
            "inglés"
        ],
        idioma="Inglés"
    ),


    Job(
        titulo="Asistente Administrativo",
        empresa="Empresa B",
        habilidades=[
            "Office",
            "organización",
            "Excel"
        ]
    ),


    Job(
        titulo="Recepcionista Bilingüe",
        empresa="Empresa C",
        habilidades=[
            "servicio al cliente",
            "inglés",
            "comunicación"
        ],
        idioma="Inglés"
    )

]



matcher = JobMatcher()



print("\n===== EMPLEOS COMPATIBLES =====\n")



for empleo in empleos:


    porcentaje = matcher.comparar(
        candidato,
        empleo
    )


    print(
        empleo.titulo
        +
        " - "
        +
        empleo.empresa
    )


    print(
        "Compatibilidad:",
        porcentaje,
        "%\n"
    )