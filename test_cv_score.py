from services.cv_score_service import CVScoreService


perfil = {
    "profesion": "Desarrollo de software",
    "habilidades": [
        "python",
        "java",
        "sql",
        "git",
        "flutter"
    ],
    "idiomas": [
        "inglés"
    ],
    "nivel": "Junior"
}


score_service = CVScoreService()

resultado = score_service.evaluar(perfil)


print("======================")
print("CV SCORE")
print("======================")

print("Puntaje:", resultado["score"])

print("\nRecomendaciones:")

if resultado["recomendaciones"]:

    for r in resultado["recomendaciones"]:
        print("-", r)

else:
    print("¡Excelente CV!")