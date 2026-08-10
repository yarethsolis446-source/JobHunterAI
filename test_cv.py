from services.cv_service import CVService



ruta = r"C:\Users\Admin\Documents\Beatbren oroginal.pdf"



servicio = CVService()



candidato = servicio.procesar_cv(
    ruta
)



candidato.mostrar()