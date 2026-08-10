from services.cv_service import CVService
from engine.search_engine import SearchEngine
from services.pdf_service import PDFService



ruta = r"C:\Users\Admin\Documents\Beatbren oroginal.pdf"



candidato = CVService().procesar_cv(
    ruta
)



engine = SearchEngine()



resultados = engine.buscar(
    candidato,
    idioma="inglés"
)



pdf = PDFService()



archivo = pdf.generar(
    candidato,
    resultados
)



print(
    "PDF creado:",
    archivo
)