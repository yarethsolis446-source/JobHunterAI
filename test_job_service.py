from services.cv_service import CVService
from services.job_service import JobService
from ai.job_matcher import JobMatcher


# Ruta del CV

ruta = r"C:\Users\Admin\Documents\Beatbren oroginal.pdf"


# Procesar CV

candidato = CVService().procesar_cv(ruta)


# Buscar empleos

empleos = JobService().buscar_empleos(candidato)


# Comparar

matcher = JobMatcher()

resultado = []


for empleo in empleos:

    score = matcher.comparar(
        candidato,
        empleo
    )

    resultado.append(
        (
            score,
            empleo
        )
    )


# Ordenar

resultado.sort(
    key=lambda x: x[0],
    reverse=True
)


print("\n=========== TOP EMPLEOS ===========\n")


for score, empleo in resultado:

    print(
        f"{empleo.titulo}"
    )

    print(
        f"Empresa: {empleo.empresa}"
    )

    print(
        f"Compatibilidad: {score}%"
    )

    print()