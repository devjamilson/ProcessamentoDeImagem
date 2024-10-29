import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os


class EqualizadorHistograma:
    def __init__(self, imagem):
        # Converte a imagem para escala de cinza
        self.imagem_original = imagem
        self.imagem_equalizada = None

    def calcular_histograma(self):
        # Calcula o histograma da imagem (256 níveis de cinza)
        histograma, _ = np.histogram(self.imagem_original, bins=256, range=(0, 256))
        return histograma

    def equalizar(self):
        # Calcula o histograma e o CDF da imagem original
        histograma = self.calcular_histograma()
        cdf = histograma.cumsum()
        cdf_normalizado = cdf / cdf[-1]  # Normalizar o CDF

        # Aplicar a transformação de equalização
        imagem_equalizada = np.floor(255 * cdf_normalizado[self.imagem_original]).astype(np.uint8)
        
        # Armazena a imagem equalizada para uso futuro
        self.imagem_equalizada = imagem_equalizada
        return self.imagem_equalizada

    def calcular_histograma_equalizado(self):
        # Calcula o histograma da imagem equalizada
        if self.imagem_equalizada is None:
            raise ValueError("A imagem ainda não foi equalizada.")
        histograma, _ = np.histogram(self.imagem_equalizada, bins=256, range=(0, 256))
        return histograma

    def plotar_resultados(self):
        # Visualizar imagem original, histograma original, imagem equalizada, e histograma equalizado
        plt.figure(figsize=(12, 6))

        # Imagem original
        plt.subplot(2, 2, 1)
        plt.imshow(self.imagem_original, cmap='gray')
        plt.title('Imagem Original')
        plt.axis('off')

        # Histograma da imagem original
        plt.subplot(2, 2, 2)
        plt.plot(self.calcular_histograma())
        plt.title('Histograma Original')

        # Imagem equalizada
        plt.subplot(2, 2, 3)
        plt.imshow(self.imagem_equalizada, cmap='gray')
        plt.title('Imagem Equalizada')
        plt.axis('off')

        # Histograma da imagem equalizada
        plt.subplot(2, 2, 4)
        plt.plot(self.calcular_histograma_equalizado())
        plt.title('Histograma Equalizado')

        plt.tight_layout()
        plt.show()

# Função para carregar uma imagem PGM com numpy
def carregar_imagem_pgm(caminho_imagem):
    """Carrega uma imagem PGM (P2 ou P5) e retorna como um array numpy."""
    if not os.path.exists(caminho_imagem):
        raise FileNotFoundError(f"O arquivo não foi encontrado: {caminho_imagem}")

    with open(caminho_imagem, 'rb') as f:
        header = f.readline().strip()
        
        # Verifica o formato (P2 para ASCII, P5 para binário)
        if header == b'P5':
            # Formato binário
            width, height = map(int, f.readline().split())
            maxval = int(f.readline().strip())
            
            # Carrega a imagem em escala de cinza
            imagem_data = np.fromfile(f, dtype=np.uint8 if maxval < 256 else np.uint16)
            imagem = imagem_data.reshape((height, width))
        
        elif header == b'P2':
            # Formato ASCII
            width, height = map(int, f.readline().split())
            maxval = int(f.readline().strip())
            
            # Carrega a imagem linha por linha em escala de cinza
            imagem_data = []
            for line in f:
                imagem_data.extend(map(int, line.split()))
            imagem = np.array(imagem_data, dtype=np.uint8).reshape((height, width))
        
        else:
            raise ValueError("Formato PGM não suportado (esperado P2 ou P5).")

    return imagem


# Carregar a imagem PGM
caminho =  r"C:\Users\jamil\OneDrive\Área de Trabalho\ProcessamentoImagem\Imagem\Utils\lena.pgm"
imagem = carregar_imagem_pgm(caminho)

# Inicializar a classe e equalizar a imagem
equalizador = EqualizadorHistograma(imagem)
imagem_equalizada = equalizador.equalizar()

# Plotar os resultados
equalizador.plotar_resultados()
