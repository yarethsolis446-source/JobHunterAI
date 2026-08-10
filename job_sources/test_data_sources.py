
from models.job import Job


class TestDataSource:

    def buscar_empleos(
        self,
        consulta=None
    ):

        empleos = [

            # =================================================
            # 1. CUSTOMER SERVICE
            # =================================================

            Job(
                titulo="Customer Service Agent",

                empresa="Amazon",

                descripcion=(
                    "Atención al cliente mediante chat, "
                    "llamadas y correo electrónico. "
                    "Se requiere inglés y buena comunicación."
                ),

                habilidades=[
                    "servicio al cliente",
                    "inglés",
                    "comunicación",
                    "office"
                ],

                experiencia=1,

                link="https://www.amazon.jobs/"
            ),

            # =================================================
            # 2. ADMINISTRACIÓN
            # =================================================

            Job(
                titulo="Administrative Assistant",

                empresa="DHL",

                descripcion=(
                    "Soporte administrativo, manejo de "
                    "documentos, correo electrónico, "
                    "office y atención al cliente."
                ),

                habilidades=[
                    "office",
                    "comunicación",
                    "adaptabilidad",
                    "organización"
                ],

                experiencia=2,

                link="https://www.dhl.com/"
            ),

            # =================================================
            # 3. RECEPCIÓN
            # =================================================

            Job(
                titulo="Receptionist",

                empresa="Hotel Costa Rica",

                descripcion=(
                    "Recepción de clientes, atención "
                    "presencial, gestión de reservas, "
                    "inglés y resolución de problemas."
                ),

                habilidades=[
                    "servicio al cliente",
                    "inglés",
                    "adaptabilidad",
                    "comunicación"
                ],

                experiencia=1,

                link="https://www.linkedin.com/jobs/"
            ),

            # =================================================
            # 4. SOPORTE TÉCNICO
            # =================================================

            Job(
                titulo="IT Support Technician",

                empresa="Microsoft",

                descripcion=(
                    "Soporte técnico a usuarios, resolución "
                    "de problemas de software y hardware, "
                    "configuración de equipos y atención "
                    "de incidencias."
                ),

                habilidades=[
                    "soporte técnico",
                    "computación",
                    "hardware",
                    "software",
                    "comunicación"
                ],

                experiencia=1,

                link="https://careers.microsoft.com/"
            ),

            # =================================================
            # 5. DESARROLLADOR
            # =================================================

            Job(
                titulo="Junior Software Developer",

                empresa="Oracle",

                descripcion=(
                    "Desarrollo y mantenimiento de aplicaciones "
                    "de software. Trabajo con programación, "
                    "bases de datos y resolución de problemas."
                ),

                habilidades=[
                    "programación",
                    "python",
                    "bases de datos",
                    "software",
                    "resolución de problemas"
                ],

                experiencia=1,

                link="https://www.oracle.com/careers/"
            ),

            # =================================================
            # 6. QA
            # =================================================

            Job(
                titulo="Junior QA Tester",

                empresa="IBM",

                descripcion=(
                    "Pruebas de aplicaciones, detección de "
                    "errores, documentación de problemas y "
                    "colaboración con equipos de desarrollo."
                ),

                habilidades=[
                    "testing",
                    "software",
                    "análisis",
                    "comunicación",
                    "resolución de problemas"
                ],

                experiencia=1,

                link="https://www.ibm.com/careers/"
            ),

            # =================================================
            # 7. MARKETING
            # =================================================

            Job(
                titulo="Marketing Assistant",

                empresa="Coca-Cola",

                descripcion=(
                    "Apoyo en campañas de marketing, creación "
                    "de contenido, análisis de resultados y "
                    "gestión de redes sociales."
                ),

                habilidades=[
                    "marketing",
                    "comunicación",
                    "redes sociales",
                    "creatividad",
                    "office"
                ],

                experiencia=1,

                link="https://www.coca-colacompany.com/careers"
            ),

            # =================================================
            # 8. VENTAS
            # =================================================

            Job(
                titulo="Sales Representative",

                empresa="Dell",

                descripcion=(
                    "Atención a clientes, presentación de "
                    "productos, seguimiento de ventas y "
                    "cumplimiento de objetivos comerciales."
                ),

                habilidades=[
                    "ventas",
                    "servicio al cliente",
                    "comunicación",
                    "negociación",
                    "office"
                ],

                experiencia=1,

                link="https://jobs.dell.com/"
            ),

            # =================================================
            # 9. DATA ENTRY
            # =================================================

            Job(
                titulo="Data Entry Specialist",

                empresa="Accenture",

                descripcion=(
                    "Ingreso y actualización de información "
                    "en sistemas empresariales, revisión de "
                    "datos y elaboración de reportes."
                ),

                habilidades=[
                    "office",
                    "excel",
                    "organización",
                    "atención al detalle",
                    "computación"
                ],

                experiencia=1,

                link="https://www.accenture.com/careers"
            ),

            # =================================================
            # 10. RECURSOS HUMANOS
            # =================================================

            Job(
                titulo="Human Resources Assistant",

                empresa="KPMG",

                descripcion=(
                    "Apoyo en procesos de recursos humanos, "
                    "gestión de documentación, comunicación "
                    "con empleados y organización de información."
                ),

                habilidades=[
                    "recursos humanos",
                    "comunicación",
                    "organización",
                    "office",
                    "adaptabilidad"
                ],

                experiencia=1,

                link="https://kpmg.com/careers"
            ),

            # =================================================
            # 11. SOPORTE AL CLIENTE
            # =================================================

            Job(
                titulo="Technical Customer Support",

                empresa="Cisco",

                descripcion=(
                    "Atención a clientes y resolución de "
                    "problemas técnicos relacionados con "
                    "productos y servicios tecnológicos."
                ),

                habilidades=[
                    "soporte técnico",
                    "servicio al cliente",
                    "inglés",
                    "comunicación",
                    "software"
                ],

                experiencia=2,

                link="https://jobs.cisco.com/"
            ),

            # =================================================
            # 12. ANALISTA DE DATOS JUNIOR
            # =================================================

            Job(
                titulo="Junior Data Analyst",

                empresa="Google",

                descripcion=(
                    "Análisis de datos, elaboración de reportes, "
                    "identificación de tendencias y apoyo en "
                    "la toma de decisiones mediante información."
                ),

                habilidades=[
                    "python",
                    "excel",
                    "análisis",
                    "bases de datos",
                    "estadística"
                ],

                experiencia=1,

                link="https://www.google.com/about/careers/"
            )
        ]

        # =====================================================
        # FILTRAR POR CONSULTA
        # =====================================================

        if consulta:

            consulta = consulta.lower()

            resultados = []

            for empleo in empleos:

                texto = (
                    empleo.titulo
                    + " "
                    + empleo.empresa
                    + " "
                    + empleo.descripcion
                    + " "
                    + " ".join(empleo.habilidades)
                ).lower()

                if consulta in texto:
                    resultados.append(empleo)

            return resultados

        return empleos
