from job_sources.base_source import BaseJobSource
from models.job import Job


class APISource(BaseJobSource):

    def __init__(self, nombre):

        self.nombre = nombre

    def buscar_empleos(self, candidato=None):

        """
        Este método será implementado por cada API.
        """

        raise NotImplementedError(
            "Cada API debe implementar buscar_empleos()."
        )

    def crear_job(
        self,
        titulo,
        empresa,
        descripcion,
        requisitos,
        habilidades,
        ubicacion,
        remoto,
        contrato,
        experiencia,
        salario,
        beneficios,
        idioma,
        link,
        fuente
    ):

        return Job(

            titulo=titulo,

            empresa=empresa,

            descripcion=descripcion,

            requisitos=requisitos,

            habilidades=habilidades,

            ubicacion=ubicacion,

            remoto=remoto,

            contrato=contrato,

            experiencia=experiencia,

            salario=salario,

            beneficios=beneficios,

            idioma=idioma,

            link=link,

            fuente=fuente

        )