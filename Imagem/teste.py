import numpy as np
import matplotlib.pyplot as plt

class VisualizadorImagemPGM:
    def __init__(self, caminho_imagem):
        self.caminho_imagem = caminho_imagem
        self.imagem = None

    def carregar_imagem(self):
        # Carrega a imagem PGM como uma matriz numpy
        with open(self.caminho_imagem, 'rb') as f:
            self.imagem = np.loadtxt(f, skiprows=3)  # Pule o cabeçalho (primeiras 3 linhas no formato PGM)

    def visualizar(self):
        if self.imagem is None:
            raise ValueError("A imagem não foi carregada. Chame o método 'carregar_imagem' primeiro.")

        # Exibe a imagem usando matplotlib
        plt.imshow(self.imagem, cmap='gray')
        plt.axis('off')  # Remove os eixos para uma visualização mais limpa
        plt.show()

# Exemplo de uso
caminho = r"C:\Users\jamil\OneDrive\Área de Trabalho\ProcessamentoImagem\Utils\lena.pgm"
visualizador = VisualizadorImagemPGM(caminho)
visualizador.carregar_imagem()
visualizador.visualizar()