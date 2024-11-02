import os
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import customtkinter as ctk
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def carregar_imagem_pgm(caminho_imagem):
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

class EqualizadorHistograma:
    def __init__(self, path: str):
        """Inicializa a classe com a imagem a ser equalizada."""
        self.imagem_original, self.maxval = carregar_imagem_pgm(path)
        self.imagem_equalizada = None

    def calcular_histograma(self):
        """Calcula o histograma da imagem original."""
        histograma, _ = np.histogram(self.imagem_original, bins=256, range=(0, 256))
        return histograma

    def equalizar(self):
        """Aplica a equalização de histograma na imagem original."""
        histograma = self.calcular_histograma()
        cdf = histograma.cumsum()
        cdf_normalizado = (cdf / cdf[-1]) * 255  

        imagem_equalizada = cdf_normalizado[self.imagem_original].astype(np.uint8)
        self.imagem_equalizada = imagem_equalizada

    def calcular_histograma_equalizado(self):
        """Calcula o histograma da imagem equalizada."""
        if self.imagem_equalizada is None:
            raise ValueError("A imagem ainda não foi equalizada.")
        histograma, _ = np.histogram(self.imagem_equalizada, bins=256, range=(0, 256))
        return histograma

    def show_images(self):
        """Mostra a imagem original, a imagem equalizada, e seus histogramas."""
        if self.imagem_equalizada is None:
            print("Primeiro aplique a equalização usando o método `equalizar`.")
            return

        plt.figure(figsize=(12, 6))
        
        # Imagem original
        plt.subplot(2, 2, 1)
        plt.title("Imagem Original")
        plt.imshow(self.imagem_original, cmap="gray")
        plt.axis("off")

        # Histograma da imagem original
        plt.subplot(2, 2, 2)
        plt.title("Histograma Original")
        plt.bar(range(256), self.calcular_histograma(), color="gray")

        # Imagem equalizada
        plt.subplot(2, 2, 3)
        plt.title("Imagem Equalizada")
        plt.imshow(self.imagem_equalizada, cmap="gray")
        plt.axis("off")

        # Histograma da imagem equalizada
        plt.subplot(2, 2, 4)
        plt.title("Histograma Equalizado")
        plt.bar(range(256), self.calcular_histograma_equalizado(), color="gray")
        
        plt.tight_layout()
        plt.show()

    def get_ctk_image(self, width=None, height=None):
        """Converte a imagem equalizada para CTkImage para uso no CustomTkinter."""
        if self.imagem_equalizada is None:
            raise ValueError("Primeiro aplique a equalização usando o método `equalizar`.")
        
        # Converte a imagem para CTkImage e mantém em memória
        imagem_tk = Image.fromarray(self.imagem_equalizada)
        self.tk_image = ctk.CTkImage(imagem_tk, size=(width, height))
        return self.tk_image