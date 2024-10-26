import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class VisualizadorImagemPGM:
    def __init__(self, caminho_imagem):
        self.caminho_imagem = caminho_imagem
        self.imagem = None

    def carregar_imagem(self):
        if not os.path.exists(self.caminho_imagem):
            raise FileNotFoundError(f"O arquivo não foi encontrado: {self.caminho_imagem}")

        try:
            # Tenta carregar a imagem usando Pillow
            self.imagem = Image.open(self.caminho_imagem)
            self.imagem = np.array(self.imagem)  # Converte para uma matriz numpy
        except Exception as e:
            print(f"Erro ao abrir a imagem com Pillow: {e}")
            # Como fallback, tenta carregar a imagem como texto
            try:
                with open(self.caminho_imagem, 'rb') as f:
                    self.imagem = np.loadtxt(f, skiprows=3)  # Pule o cabeçalho
            except Exception as e:
                raise ValueError(f"Erro ao carregar a imagem como matriz numpy: {e}")

    def visualizar(self):
        if self.imagem is None:
            raise ValueError("A imagem não foi carregada. Chame o método 'carregar_imagem' primeiro.")

        # Exibe a imagem usando matplotlib
        plt.imshow(self.imagem, cmap='gray')
        plt.axis('off')  # Remove os eixos para uma visualização mais limpa
        plt.show()

    def salvar_imagem(self, caminho_saida):
        if self.imagem is None:
            raise ValueError("A imagem não foi carregada. Chame o método 'carregar_imagem' primeiro.")

        # Salva a imagem utilizando PIL para garantir a compatibilidade
        imagem_pil = Image.fromarray(self.imagem.astype(np.uint8))  # Converte a matriz numpy de volta para uma imagem
        imagem_pil.save(caminho_saida)

