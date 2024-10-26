# imagens/imagem_base.py
import numpy as np
from PIL import Image

class ImagemBase:
    def __init__(self, caminho_imagem):
        self.caminho_imagem = caminho_imagem
        self.imagem = None
        self.carregar_imagem()

    def carregar_imagem(self):
        """Carrega a imagem do caminho especificado."""
        self.imagem = np.array(Image.open(self.caminho_imagem))

    def salvar_imagem(self, caminho_saida):
        """Salva a imagem em um novo caminho."""
        Image.fromarray(self.imagem).save(caminho_saida)

    def mostrar(self):
        """Exibe a imagem."""
        Image.fromarray(self.imagem).show()
