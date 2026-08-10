from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)
from reportlab.lib import colors
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
)
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from xml.sax.saxutils import escape


class PDFGenerator:

    def __init__(self):

        self.styles = getSampleStyleSheet()

        self.titulo = ParagraphStyle(
            "Titulo",
            parent=self.styles["Title"],
            fontSize=22,
            leading=26,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#2563EB"),
            spaceAfter=8,
        )

        self.subtitulo = ParagraphStyle(
            "Subtitulo",
            parent=self.styles["Heading2"],
            fontSize=15,
            leading=18,
            textColor=colors.HexColor("#1E3A8A"),
            spaceBefore=12,
            spaceAfter=10,
        )

        self.normal = ParagraphStyle(
            "NormalPersonalizado",
            parent=self.styles["BodyText"],
            fontSize=9.5,
            leading=13,
            spaceAfter=5,
        )

        self.empleo_titulo = ParagraphStyle(
            "EmpleoTitulo",
            parent=self.styles["Heading3"],
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#111827"),
            spaceAfter=5,
        )

        self.pequeno = ParagraphStyle(
            "Pequeno",
            parent=self.styles["BodyText"],
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#6B7280"),
        )

        self.campo = ParagraphStyle(
            "Campo",
            parent=self.normal,
            fontSize=9.5,
            leading=13,
        )

    # =========================================================
    # FUNCIONES AUXILIARES
    # =========================================================

    def limpiar_texto(self, texto):

        if texto is None:
            return ""

        return escape(str(texto))

    def lista_texto(self, lista):

        if not lista:
            return ""

        return ", ".join(
            self.limpiar_texto(item)
            for item in lista
        )

    # =========================================================
    # GENERAR PDF
    # =========================================================

    def generar(
        self,
        ruta,
        perfil,
        empleos,
    ):

        documento = SimpleDocTemplate(
            ruta,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40,
            title="JobHunter AI - Reporte de compatibilidad",
            author="JobHunter AI",
        )

        elementos = []

        # =====================================================
        # TITULO
        # =====================================================

        elementos.append(
            Paragraph(
                "JOBHUNTER AI",
                self.titulo,
            )
        )

        elementos.append(
            Paragraph(
                "Reporte de compatibilidad laboral",
                self.normal,
            )
        )

        elementos.append(
            Spacer(1, 15)
        )

        # =====================================================
        # PERFIL
        # =====================================================

        elementos.append(
            Paragraph(
                "Perfil del candidato",
                self.subtitulo,
            )
        )

        habilidades = perfil.get(
            "habilidades",
            [],
        )

        idiomas = perfil.get(
            "idiomas",
            [],
        )

        educacion = perfil.get(
            "educacion",
            {},
        )

        datos_perfil = [

            [
                Paragraph(
                    "<b>Profesión</b>",
                    self.campo,
                ),

                Paragraph(
                    self.limpiar_texto(
                        perfil.get(
                            "profesion",
                            "No especificada",
                        )
                    ),
                    self.campo,
                ),
            ],

            [
                Paragraph(
                    "<b>Nivel</b>",
                    self.campo,
                ),

                Paragraph(
                    self.limpiar_texto(
                        perfil.get(
                            "nivel",
                            "No especificado",
                        )
                    ),
                    self.campo,
                ),
            ],

            [
                Paragraph(
                    "<b>Experiencia</b>",
                    self.campo,
                ),

                Paragraph(
                    str(
                        perfil.get(
                            "experiencia",
                            0,
                        )
                    ) + " años",
                    self.campo,
                ),
            ],

            [
                Paragraph(
                    "<b>Idiomas</b>",
                    self.campo,
                ),

                Paragraph(
                    self.lista_texto(
                        idiomas
                    )
                    or "No especificados",
                    self.campo,
                ),
            ],

            [
                Paragraph(
                    "<b>Habilidades</b>",
                    self.campo,
                ),

                Paragraph(
                    self.lista_texto(
                        habilidades
                    )
                    or "No especificadas",
                    self.campo,
                ),
            ],
        ]

        tabla_perfil = Table(
            datos_perfil,
            colWidths=[
                1.4 * inch,
                5.3 * inch,
            ],
            repeatRows=0,
        )

        tabla_perfil.setStyle(
            TableStyle(
                [

                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        colors.HexColor(
                            "#EFF6FF"
                        ),
                    ),

                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (0, -1),
                        colors.HexColor(
                            "#1E3A8A"
                        ),
                    ),

                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.HexColor(
                            "#D1D5DB"
                        ),
                    ),

                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),

                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),

                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),

                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                ]
            )
        )

        elementos.append(
            tabla_perfil
        )

        elementos.append(
            Spacer(1, 18)
        )

        # =====================================================
        # EDUCACION
        # =====================================================

        if educacion:

            elementos.append(
                Paragraph(
                    "Educación y certificaciones",
                    self.subtitulo,
                )
            )

            educacion_texto = []

            for clave, valor in educacion.items():

                if valor:

                    nombre = (
                        str(clave)
                        .replace(
                            "_",
                            " ",
                        )
                        .title()
                    )

                    educacion_texto.append(
                        nombre
                    )

            if educacion_texto:

                elementos.append(
                    Paragraph(
                        " • ".join(
                            educacion_texto
                        ),
                        self.normal,
                    )
                )

        # =====================================================
        # EMPLEOS
        # =====================================================

        elementos.append(
            Spacer(1, 10)
        )

        elementos.append(
            Paragraph(
                "Empleos recomendados",
                self.subtitulo,
            )
        )

        elementos.append(
            Paragraph(
                f"Se encontraron "
                f"<b>{len(empleos)}</b> "
                "empleos compatibles con "
                "el perfil.",
                self.normal,
            )
        )

        elementos.append(
            Spacer(1, 10)
        )

        # =====================================================
        # CADA EMPLEO
        # =====================================================

        for posicion, empleo in enumerate(
            empleos,
            start=1,
        ):

            titulo = empleo.get(
                "titulo",
                "Puesto sin especificar",
            )

            empresa = empleo.get(
                "empresa",
                "Empresa no especificada",
            )

            score = empleo.get(
                "score",
                0,
            )

            nivel = empleo.get(
                "nivel",
                "No especificado",
            )

            descripcion = empleo.get(
                "descripcion",
                "",
            )

            ubicacion = empleo.get(
                "ubicacion",
                "",
            )

            salario = empleo.get(
                "salario",
                "",
            )

            coincidencias = empleo.get(
                "coincidencias",
                [],
            )

            faltantes = empleo.get(
                "faltantes",
                [],
            )

            explicacion = empleo.get(
                "explicacion",
                [],
            )

            link = empleo.get(
                "link",
                "",
            )

            # =================================================
            # COLOR
            # =================================================

            if score >= 85:

                color_fondo = (
                    colors.HexColor(
                        "#ECFDF5"
                    )
                )

                color_score = "#15803D"

            elif score >= 65:

                color_fondo = (
                    colors.HexColor(
                        "#FFFBEB"
                    )
                )

                color_score = "#B45309"

            else:

                color_fondo = (
                    colors.HexColor(
                        "#FEF2F2"
                    )
                )

                color_score = "#DC2626"

            # =================================================
            # CONTENIDO DEL EMPLEO
            # =================================================

            elementos.append(
                Paragraph(
                    f"{posicion}. "
                    f"{self.limpiar_texto(titulo)}",
                    self.empleo_titulo,
                )
            )

            elementos.append(
                Paragraph(
                    f"<b>Empresa:</b> "
                    f"{self.limpiar_texto(empresa)}",
                    self.normal,
                )
            )

            elementos.append(
                Paragraph(
                    f'<b>Compatibilidad:</b> '
                    f'<font color="{color_score}">'
                    f'<b>{score}%</b>'
                    f"</font>",
                    self.normal,
                )
            )

            elementos.append(
                Paragraph(
                    f"<b>Nivel:</b> "
                    f"{self.limpiar_texto(nivel)}",
                    self.normal,
                )
            )

            # =================================================
            # UBICACION
            # =================================================

            if ubicacion:

                elementos.append(
                    Paragraph(
                        f"<b>Ubicación:</b> "
                        f"{self.limpiar_texto(ubicacion)}",
                        self.normal,
                    )
                )

            # =================================================
            # SALARIO
            # =================================================

            if salario:

                elementos.append(
                    Paragraph(
                        f"<b>Salario:</b> "
                        f"{self.limpiar_texto(salario)}",
                        self.normal,
                    )
                )

            # =================================================
            # DESCRIPCION
            # =================================================

            if descripcion:

                elementos.append(
                    Paragraph(
                        "<b>Descripción:</b> "
                        + self.limpiar_texto(
                            descripcion
                        ),
                        self.normal,
                    )
                )

            # =================================================
            # COINCIDENCIAS
            # =================================================

            if coincidencias:

                elementos.append(
                    Paragraph(
                        "<b>✓ Habilidades "
                        "coincidentes:</b> "
                        + self.lista_texto(
                            coincidencias
                        ),
                        self.normal,
                    )
                )

            else:

                elementos.append(
                    Paragraph(
                        "<b>✓ Habilidades "
                        "coincidentes:</b> "
                        "Ninguna",
                        self.normal,
                    )
                )

            # =================================================
            # FALTANTES
            # =================================================

            if faltantes:

                elementos.append(
                    Paragraph(
                        "<b>⚠ Habilidades "
                        "faltantes:</b> "
                        + self.lista_texto(
                            faltantes
                        ),
                        self.normal,
                    )
                )

            else:

                elementos.append(
                    Paragraph(
                        "<b>✓ Habilidades "
                        "faltantes:</b> "
                        "Ninguna",
                        self.normal,
                    )
                )

            # =================================================
            # EXPLICACION
            # =================================================

            if explicacion:

                elementos.append(
                    Paragraph(
                        "<b>Explicación "
                        "del resultado:</b>",
                        self.normal,
                    )
                )

                for razon in explicacion:

                    elementos.append(
                        Paragraph(
                            "• "
                            + self.limpiar_texto(
                                razon
                            ),
                            self.normal,
                        )
                    )

            # =================================================
            # LINK
            # =================================================

            if link:

                link_seguro = str(
                    link
                ).strip()

                elementos.append(
                    Paragraph(
                        f'<link href="{link_seguro}" '
                        f'color="#2563EB">'
                        f'<u>Abrir oferta de empleo</u>'
                        f"</link>",
                        self.normal,
                    )
                )

            else:

                elementos.append(
                    Paragraph(
                        "Oferta sin enlace disponible.",
                        self.normal,
                    )
                )

            # =================================================
            # LINEA VISUAL
            # =================================================

            separador = Table(
                [
                    [
                        ""
                    ]
                ],
                colWidths=[
                    6.7 * inch
                ],
                rowHeights=[
                    5
                ],
            )

            separador.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, -1),
                            color_fondo,
                        ),

                        (
                            "BOX",
                            (0, 0),
                            (-1, -1),
                            1,
                            colors.HexColor(
                                "#CBD5E1"
                            ),
                        ),
                    ]
                )
            )

            elementos.append(
                separador
            )

            elementos.append(
                Spacer(1, 10)
            )

        # =====================================================
        # PIE
        # =====================================================

        elementos.append(
            Spacer(1, 15)
        )

        elementos.append(
            Paragraph(
                "Reporte generado automáticamente "
                "por JobHunter AI.",
                self.pequeno,
            )
        )

        # =====================================================
        # CONSTRUIR PDF
        # =====================================================

        try:

            documento.build(
                elementos
            )

            print(
                "\n=============================="
            )

            print(
                "PDF GENERADO CORRECTAMENTE"
            )

            print(
                "=============================="
            )

            print(
                f"Ruta: {ruta}"
            )

            return True

        except Exception as error:

            print(
                "\n=============================="
            )

            print(
                "ERROR GENERANDO PDF:"
            )

            print(
                error
            )

            print(
                "=============================="
            )

            return False