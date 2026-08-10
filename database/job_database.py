from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet



class PDFService:


    def generar(
        self,
        candidato,
        resultados,
        ruta_salida="JobHunter_AI_Resultados.pdf"
    ):


        documento = SimpleDocTemplate(
            ruta_salida,
            pagesize=letter
        )


        estilos = getSampleStyleSheet()


        contenido = []



        # =========================
        # PORTADA
        # =========================


        contenido.append(
            Paragraph(
                "JOBHUNTER AI",
                estilos["Title"]
            )
        )


        contenido.append(
            Spacer(1, 20)
        )


        contenido.append(
            Paragraph(
                "Reporte personalizado de oportunidades laborales",
                estilos["Heading2"]
            )
        )


        contenido.append(
            Spacer(1, 30)
        )



        contenido.append(
            Paragraph(
                f"<b>Candidato:</b> {candidato.nombre}",
                estilos["BodyText"]
            )
        )



        contenido.append(
            Paragraph(
                f"<b>Empleos analizados:</b> {len(resultados)}",
                estilos["BodyText"]
            )
        )


        contenido.append(
            Spacer(1, 40)
        )



        contenido.append(
            Paragraph(
                "TOP EMPLEOS RECOMENDADOS",
                estilos["Heading2"]
            )
        )


        contenido.append(
            Spacer(1, 20)
        )



        # =========================
        # EMPLEOS
        # =========================


        posicion = 1



        for resultado in resultados:


            empleo = resultado.empleo



            titulo = f"""

            <b>
            {posicion}. {empleo.titulo}
            </b>

            """



            contenido.append(

                Paragraph(
                    titulo,
                    estilos["Heading3"]
                )

            )



            informacion = f"""

            <b>Empresa:</b>
            {empleo.empresa}
            <br/>


            <b>Compatibilidad:</b>
            {resultado.score}%
            <br/>


            <b>Nivel:</b>
            {resultado.nivel}
            <br/><br/>


            <b>Descripción:</b>
            <br/>
            {empleo.descripcion}
            <br/><br/>


            <b>Ubicación:</b>
            {empleo.ubicacion}
            <br/>


            <b>Modalidad:</b>
            {"Remoto" if empleo.remoto else "Presencial"}
            <br/>


            <b>Contrato:</b>
            {empleo.contrato}
            <br/>


            <b>Experiencia requerida:</b>
            {empleo.experiencia}
            <br/>


            <b>Salario:</b>
            {empleo.salario}
            <br/><br/>


            <b>Coincidencias con tu perfil:</b>
            <br/>

            {self.lista(
                resultado.coincidencias
            )}

            <br/>


            <b>Habilidades faltantes:</b>
            <br/>

            {self.lista(
                resultado.faltantes
            )}

            <br/>


            <b>Requisitos:</b>
            <br/>

            {self.lista(
                empleo.requisitos
            )}

            <br/>


            <b>Beneficios:</b>
            <br/>

            {self.lista(
                empleo.beneficios
            )}

            <br/><br/>


            <a href="{empleo.link}" color="blue">
            🔗 Aplicar al puesto
            </a>


            """



            contenido.append(

                Paragraph(
                    informacion,
                    estilos["BodyText"]
                )

            )



            contenido.append(
                Spacer(1, 35)
            )



            posicion += 1



            # Separar páginas cada cierto número

            if posicion % 5 == 0:

                contenido.append(
                    PageBreak()
                )



        documento.build(
            contenido
        )



        return ruta_salida




    def lista(
        self,
        elementos
    ):


        if not elementos:

            return "Ninguno"



        texto = ""


        for elemento in elementos:

            texto += f"• {elemento}<br/>"



        return texto