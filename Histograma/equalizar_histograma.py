import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import customtkinter as ctk
from PIL import Image, ImageTk
import os

class EqualizadorHistograma:
    def __init__(self, imagem):
        self.imagem_original = imagem
        self.imagem_equalizada = None

    def calcular_histograma(self):
        histograma, _ = np.histogram(self.imagem_original, bins=256, range=(0, 256))
        return histograma

    def equalizar(self):
        histograma = self.calcular_histograma()
        cdf = histograma.cumsum()
        cdf_normalizado = cdf / cdf[-1]  

        imagem_equalizada = np.floor(255 * cdf_normalizado[self.imagem_original]).astype(np.uint8)
        
        self.imagem_equalizada = imagem_equalizada
        return self.imagem_equalizada

    def calcular_histograma_equalizado(self):
        if self.imagem_equalizada is None:
            raise ValueError("A imagem ainda não foi equalizada.")
        histograma, _ = np.histogram(self.imagem_equalizada, bins=256, range=(0, 256))
        return histograma

    def plotar_resultados(self, tab):
        """Exibe a imagem original, imagem equalizada, e seus histogramas como gráficos de barra em um Canvas Tkinter."""
        fig, axs = plt.subplots(2, 2, figsize=(12, 6))

        # Imagem original
        axs[0, 0].imshow(self.imagem_original, cmap='gray')
        axs[0, 0].set_title('Imagem Original')
        axs[0, 0].axis('off')

        # Histograma da imagem original
        histograma_original = self.calcular_histograma()
        axs[0, 1].bar(range(256), histograma_original, color='gray')
        axs[0, 1].set_title('Histograma Original')

        # Imagem equalizada
        axs[1, 0].imshow(self.imagem_equalizada, cmap='gray')
        axs[1, 0].set_title('Imagem Equalizada')
        axs[1, 0].axis('off')

        # Histograma da imagem equalizada
        histograma_equalizado = self.calcular_histograma_equalizado()
        axs[1, 1].bar(range(256), histograma_equalizado, color='gray')
        axs[1, 1].set_title('Histograma Equalizado')

        fig.tight_layout()

        # Converte a figura para uma imagem compatível com Tkinter
        canvas = FigureCanvas(fig)
        canvas.draw()
        image = Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
        image_tk = ImageTk.PhotoImage(image)

        # Exibe a imagem no tab especificado
        label = ctk.CTkLabel(tab, image=image_tk)
        label.image = image_tk  # Armazena uma referência para evitar que o GC limpe
        label.pack(pady=10)


def carregar_imagem_pgm(caminho_imagem):
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
            
            imagem_data = []
            for line in f:
                imagem_data.extend(map(int, line.split()))
            imagem = np.array(imagem_data, dtype=np.uint8).reshape((height, width))
        
        else:
            raise ValueError("Formato PGM não suportado (esperado P2 ou P5).")

    return imagem

