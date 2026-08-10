from ai.extractors.education_extractor import EducationExtractor

texto = """
Bachelor in Software Engineering

University of Costa Rica

AWS Certified Developer

Docker

Kubernetes

Scrum Master

Python Bootcamp
"""

extractor = EducationExtractor()

resultado = extractor.extraer(texto)

print(resultado)