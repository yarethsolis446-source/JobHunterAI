from ai.extractors.lenguage_extractor import LanguageExtractor


texto = """
Software Developer

English C1
Español nativo
French B2
"""


extractor = LanguageExtractor()


resultado = extractor.extraer(texto)


print(resultado)