import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class VisualizadorImagemPGM:
    def __init__(self, caminho_imagem):
        self.caminho_imagem = caminho_imagem

    def visualizar(self):
        """Carrega e visualiza a imagem PGM a partir do caminho fornecido."""
        if not os.path.exists(self.caminho_imagem):
            raise FileNotFoundError(f"O arquivo não foi encontrado: {self.caminho_imagem}")

        try:
            # Tenta carregar a imagem usando Pillow
            imagem = Image.open(self.caminho_imagem)
            imagem = np.array(imagem)  # Converte para uma matriz numpy
        except Exception as e:
            print(f"Erro ao abrir a imagem com Pillow: {e}")
            # Como fallback, tenta carregar a imagem como texto
            try:
                with open(self.caminho_imagem, 'rb') as f:
                    imagem = np.loadtxt(f, skiprows=3)  # Pule o cabeçalho
            except Exception as e:
                raise ValueError(f"Erro ao carregar a imagem como matriz numpy: {e}")

        # Exibe a imagem usando matplotlib
        plt.imshow(imagem, cmap='gray')
        plt.axis('off')  # Remove os eixos para uma visualização mais limpa
        plt.show()

# Exemplo de uso
caminho_imagem = r"C:\Users\jamil\OneDrive\Área de Trabalho\ProcessamentoImagem\Imagem\imagem_filtrada.pgm"
visualizador = VisualizadorImagemPGM(caminho_imagem)
visualizador.visualizar()
