from abc import ABC, abstractmethod


class BaseJobSource(ABC):

    @abstractmethod
    def buscar_empleos(self, candidato=None):
        """
        Debe devolver una lista de objetos Job.
        """
        pass