import numpy as np

class FiltroBase:
    def aplicar(self, imagem):
        """Método a ser implementado pelos filtros específicos."""
        raise NotImplementedError("Este método deve ser implementado por filtros específicos.")
