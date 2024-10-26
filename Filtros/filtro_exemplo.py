# filtros/filtro_exemplo.py
import numpy as np
from .filtro_base import FiltroBase

class FiltroExemplo(FiltroBase):
    def aplicar(self, imagem):
        """Aplica um filtro simples (por exemplo, inversão de cores)."""
        return 255 - imagem
