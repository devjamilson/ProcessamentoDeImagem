# negativo.py
import os
import numpy as np
from PIL import Image

class ProcessamentoImagemNegativo:
    def __init__(self, caminho):
        self.caminho = caminho
        self.imagem, self.maxval = self.carregar_imagem_pgm(caminho)

    def carregar_imagem_pgm(self, caminho_imagem):
        """Carrega uma imagem PGM (P2 ou P5) e retorna como um array numpy e o valor máximo de intensidade."""
        if not os.path.exists(caminho_imagem):
            raise FileNotFoundError(f"O arquivo não foi encontrado: {caminho_imagem}")

        with open(caminho_imagem, 'rb') as f:
            header = f.readline().strip()
            if header == b'P5':
                width, height = map(int, f.readline().split())
                maxval = int(f.readline().strip())
                imagem_data = np.fromfile(f, dtype=np.uint8 if maxval < 256 else np.uint16)
                imagem = imagem_data.reshape((height, width))
            elif header == b'P2':
                width, height = map(int, f.readline().split())
                maxval = int(f.readline().strip())
                imagem_data = [int(i) for line in f for i in line.split()]
                imagem = np.array(imagem_data, dtype=np.uint8).reshape((height, width))
            else:
                raise ValueError("Formato PGM não suportado (esperado P2 ou P5).")
        return imagem, maxval

    def negativo(self):
        """Gera o negativo da imagem carregada usando a transformação s = L - 1 - r."""
        negativo_array = self.maxval - self.imagem
        return Image.fromarray(negativo_array)
