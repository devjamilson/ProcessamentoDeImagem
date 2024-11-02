import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import customtkinter as ctk

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

class Gama:
    def __init__(self, caminho: str):
        """Inicializa a classe com o caminho da imagem."""
        self.imagem, self.maxval = carregar_imagem_pgm(caminho)
        self.imagem_transformada = None

    def apply_gamma(self, c: float, gamma: float):
        """Aplica a transformação gamma à imagem."""
        # Normaliza os valores da imagem para o intervalo [0, 1]
        imagem_normalizada = self.imagem / self.maxval
        
        # Aplica a transformação gamma: S = c * r^gamma
        imagem_transformada = c * np.power(imagem_normalizada, gamma)
        
        # Reescala de volta para o intervalo [0, 255]
        self.imagem_transformada = np.clip(imagem_transformada * self.maxval, 0, self.maxval).astype(np.uint8)

    def show_images(self):
        """Mostra a imagem original e a imagem transformada."""
        if self.imagem_transformada is None:
            print("Primeiro aplique a transformação gamma usando o método `transformar_gamma`.")
            return
        
        # Configurações para mostrar as imagens lado a lado
        plt.figure(figsize=(10, 5))
        
        # Imagem original
        plt.subplot(1, 2, 1)
        plt.title("Imagem Original")
        plt.imshow(self.imagem, cmap="gray")
        plt.axis("off")
        
        # Imagem transformada
        plt.subplot(1, 2, 2)
        plt.title("Imagem Transformada (Gamma)")
        plt.imshow(self.imagem_transformada, cmap="gray")
        plt.axis("off")
        
        plt.show()

    def get_ctk_image(self, width=None, height=None):
        """Converte a imagem transformada para CTkImage para uso no CustomTkinter."""
        if self.imagem_transformada is None:
            raise ValueError("Primeiro aplique a transformação gamma usando o método `transformar_gamma`.")
        
        # Converte a imagem transformada para CTkImage e mantém em memória
        self.tk_image = ctk.CTkImage(Image.fromarray(self.imagem_transformada), size=(width, height))
        return self.tk_image
